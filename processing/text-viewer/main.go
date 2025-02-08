package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    "html/template"
    "log"
    "net/http"
    "strconv"

    _ "github.com/mattn/go-sqlite3"
)

// Row represents a single row from the dataframe table.
type Row struct {
    Index        int
    Timestamp string
    Author    string
    Message   string
    Status    string
}

// db is a global pointer to the database connection
var db *sql.DB

func main() {
    var err error

    // Open (or create) the SQLite database file
    db, err = sql.Open("sqlite3", "./mydb.sqlite")
    if err != nil {
        log.Fatal("Failed to open database:", err)
    }
    defer db.Close()

    // Ensure the database is accessible
    if err = db.Ping(); err != nil {
        log.Fatal("Failed to ping database:", err)
    }

    // Define handlers
    http.HandleFunc("/", indexHandler)
    http.HandleFunc("/mark-seen", markSeenHandler)

    fmt.Println("Server running on http://localhost:8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}

// indexHandler fetches all rows from the dataframe table and displays them
func indexHandler(w http.ResponseWriter, r *http.Request) {
    // Query all rows
    rows, err := db.Query(`SELECT "index", "timestamp", "author", "message", "status" FROM dataframe ORDER BY "index"`)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer rows.Close()

    var data []Row

    // Iterate over rows and scan into our Row struct
    for rows.Next() {
        var rowObj Row
        err := rows.Scan(&rowObj.Index, &rowObj.Timestamp, &rowObj.Author, &rowObj.Message, &rowObj.Status)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
        data = append(data, rowObj)
    }

    // Use an inline template for brevity; you can use template.ParseFiles(...) instead
        tmpl := `
<html>
<head>
    <title>Dataframe Status</title>
    <script>
        // This function is called when the "Mark as Seen" button is clicked
        // It sends a POST request to /mark-seen and, if successful,
        // updates the DOM so we don't need to reload the page.
        function markAsSeen(rowId) {
            fetch('/mark-seen?id=' + rowId, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the DOM to reflect the new status
                    document.getElementById('status-' + rowId).textContent = 'seen';
                    // Disable the button
                    document.getElementById('seen-btn-' + rowId).disabled = true;
                    document.getElementById('seen-btn-' + rowId).textContent = "Already Seen";
                } else {
                    alert('Failed to mark as seen: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error marking as seen:', error);
                alert('Error marking as seen');
            });
        }
    </script>
</head>
<body>
    <h1>Dataframe Rows</h1>
    {{range .}}
        <div style="margin-bottom: 20px;">
            <p>
                <strong>ID:</strong> {{.Index}}<br>
                <strong>Timestamp:</strong> {{.Timestamp}}<br>
                <strong>Author:</strong> {{.Author}}<br>
                <strong>Message:</strong> {{.Message}}<br>
                <strong>Status:</strong> <span id="status-{{.Index}}">{{.Status}}</span>
            </p>
            {{if eq .Status "seen"}}
                <!-- If it's already seen, disable the button -->
                <button id="seen-btn-{{.Index}}" disabled>Already Seen</button>
            {{else}}
                <!-- Otherwise, attach the onClick handler -->
                <button id="seen-btn-{{.Index}}" onclick="markAsSeen({{.Index}})">
                    Mark as Seen
                </button>
            {{end}}
        </div>
    {{end}}
</body>
</html>`

    // Parse and execute the template
    t := template.Must(template.New("index").Parse(tmpl))
    if err := t.Execute(w, data); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
    }
}

func markSeenHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
        return
    }

    // Retrieve 'id' via URL query param or form (we're using query here)
    rowID := r.URL.Query().Get("id")
    if rowID == "" {
        http.Error(w, "Missing id parameter", http.StatusBadRequest)
        return
    }
    idInt, err := strconv.Atoi(rowID)
    if err != nil {
        http.Error(w, "Invalid id format", http.StatusBadRequest)
        return
    }

    // Update the database
    _, err = db.Exec(`UPDATE dataframe SET status = 'seen' WHERE "index" = ?`, idInt)
    if err != nil {
        // Return JSON error
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]interface{}{
            "success": false,
            "error":   err.Error(),
        })
        return
    }

    // Return JSON success
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]bool{"success": true})
}


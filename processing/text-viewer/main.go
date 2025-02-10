package main

import (
	"context"
	"database/sql"
	_ "embed"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
	_ "github.com/mattn/go-sqlite3"
	"conall/text-viewer/components"
	"conall/text-viewer/model"
)


var db *sql.DB

func main() {
	var err error
	db, err = sql.Open("sqlite3", "./mydb.sqlite")
	if err != nil {
		log.Fatal("Failed to open database:", err)
	}
	defer db.Close()

	if err = db.Ping(); err != nil {
		log.Fatal("Failed to ping database:", err)
	}

	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/mark-seen", markSeenHandler)

	fmt.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// indexHandler fetches all rows from the dataframe table and displays them.
// Optionally filters by month if a "?month=YYYY-MM" query param is provided.
func indexHandler(response http.ResponseWriter, request *http.Request) {
	// 1. Get the distinct months (for the dropdown)
	months, err := getDistinctMonths()
	if err != nil {
	    http.Error(response, err.Error(), http.StatusInternalServerError)
	    return
	}

	// 2. Check if a month filter is provided
	selectedMonth := request.URL.Query().Get("month") // e.g. "2023-09"

	// 3. Retrieve rows (filtered by month if provided)
	var rows *sql.Rows
	if selectedMonth != "" {
		query := `
            SELECT "index",
                   "timestamp",
                   "author",
                   "message",
                   "type",
                   COALESCE("attachment_type", '') AS "attachment_type",
                   COALESCE("image_description", '') AS "image_description",
                   COALESCE("audio_transcript", '') AS "audio_transcript",
                   "status"
            FROM dataframe
            WHERE strftime('%Y-%m', "timestamp") = ?
            ORDER BY "index"
        `
		rows, err = db.Query(query, selectedMonth)
		// ...
	} else {
		query := `
            SELECT "index",
                   "timestamp",
                   "author",
                   "message",
                   "type",
                   COALESCE("attachment_type", '') AS "attachment_type",
                   COALESCE("image_description", '') AS "image_description",
                   COALESCE("audio_transcript", '') AS "audio_transcript",
                   "status"
            FROM dataframe
            ORDER BY "index"
        `
		rows, err = db.Query(query)
		// ...
	}

	if err != nil {
		http.Error(response, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var data []model.Row
	for rows.Next() {
		var rowObj model.Row
		if err := rows.Scan(&rowObj.Index, &rowObj.Timestamp, &rowObj.Author, &rowObj.Message, &rowObj.Type, &rowObj.AttachmentType, &rowObj.ImageDescription, &rowObj.AudioTranscript, &rowObj.Status); err != nil {
			http.Error(response, err.Error(), http.StatusInternalServerError)
			return
		}
		data = append(data, rowObj)
	}
	root := components.Html(data, months, selectedMonth)

	root.Render(context.Background(), response)
}

// markSeenHandler updates one row's status to "seen".
func markSeenHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

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

	_, err = db.Exec(`UPDATE dataframe SET status = 'seen' WHERE "index" = ?`, idInt)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"success": false,
			"error":   err.Error(),
		})
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]bool{"success": true})
}

// getDistinctMonths returns a list of distinct months from "timestamp" in YYYY-MM format,
// sorted, and also creates a user-friendly label (e.g. "September 2023").
func getDistinctMonths() ([]model.MonthOption, error) {
	rows, err := db.Query(`
        SELECT DISTINCT strftime('%Y-%m', "timestamp") AS yearmonth
        FROM dataframe
        WHERE "timestamp" IS NOT NULL
        ORDER BY yearmonth
    `)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []model.MonthOption
	for rows.Next() {
		var yearMonth string
		if err := rows.Scan(&yearMonth); err != nil {
			return nil, err
		}

		// Convert e.g. "2023-09" -> "September 2023" for the label
		label := yearMonth
		if t, parseErr := time.Parse("2006-01", yearMonth); parseErr == nil {
			label = t.Format("January 2006")
		}

		results = append(results, model.MonthOption{
			YearMonth: yearMonth,
			Label:     label,
		})
	}
	return results, nil
}

package model

// Row represents a single row from the dataframe table.
type Row struct {
	Index            int
	Timestamp        string
	Author           string
	Message          string
	Type             string
	AttachmentType   string
	ImageDescription string
	AudioTranscript  string
	Status           string
}

func (row Row) ToText() TextMessage {
	return TextMessage{
		Index: row.Index,
		Timestamp: row.Timestamp,
		Author: row.Author,
		Message: row.Message,
		Status: row.Status,
	}
}

func (row Row) ToAttachment() Attachment {
	return Attachment{
		Index: row.Index,
		Timestamp: row.Timestamp,
		Author: row.Author,
		FilePath: row.Message,
		AttachmentType: row.AttachmentType,
		ImageDescription: row.ImageDescription,
		AudioTranscript: row.AudioTranscript,
		Status: row.Status,
	}
}

type TextMessage struct {
	Index            int
	Timestamp        string
	Author           string
	Message          string
	Status           string
}


type Attachment struct {
	Index            int
	Timestamp        string
	Author           string
	FilePath          string
	AttachmentType   string
	ImageDescription string
	AudioTranscript  string
	Status           string
}


type AudioMessage struct {
	Index            int
	Timestamp        string
	Author           string
	Message          string
	Type             string
	AttachmentType   string
	ImageDescription string
	AudioTranscript  string
	Status           string
}

type ImageMessage struct {
	Index            int
	Timestamp        string
	Author           string
	Message          string
	Type             string
	AttachmentType   string
	ImageDescription string
	AudioTranscript  string
	Status           string
}

// MonthOption holds data for each distinct month in the DB
type MonthOption struct {
	YearMonth string // e.g. "2023-09"
	Label     string // e.g. "September 2023"
}

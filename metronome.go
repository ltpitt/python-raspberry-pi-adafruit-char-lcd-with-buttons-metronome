package main

import (
    "fmt"
    "time"
    "sync"
    "gopkg.in/ini.v1"
    "os"
    "path/filepath"
    "github.com/faiface/beep"
    "github.com/faiface/beep/speaker"
    "github.com/faiface/beep/wav"
)

func playBeep(soundPath string, wg *sync.WaitGroup) {
    defer wg.Done()

    f, err := os.Open(soundPath)
    if err != nil {
        fmt.Printf("Failed to open sound file: %v\n", err)
        return
    }
    defer f.Close()

    streamer, _, err := wav.Decode(f)
    if err != nil {
        fmt.Printf("Failed to decode sound file: %v\n", err)
        return
    }
    defer streamer.Close()

    done := make(chan bool)
    speaker.Play(beep.Seq(streamer, beep.Callback(func() {
        done <- true
    })))
    <-done
}

func runMetronome(bpm int, isMetronomeEnabled bool, soundPath string) {
    ticker := time.NewTicker(time.Minute / time.Duration(bpm))
    defer ticker.Stop()

    wg := &sync.WaitGroup{}
    for {
        select {
        case <-ticker.C:
            if isMetronomeEnabled {
                fmt.Println("Tick") // Log every click

                wg.Add(1)
                go playBeep(soundPath, wg)
            }
        }
    }

    wg.Wait() // Ensure all goroutines complete
    speaker.Close()
}

func loadConfig() (int, bool, string) {
    configFilePath := filepath.Join(filepath.Dir(os.Args[0]), "config.cfg")
    cfg, err := ini.Load(configFilePath)
    if err != nil {
        fmt.Printf("Failed to load config file: %v\n", err)
        os.Exit(1)
    }

    bpm := cfg.Section("metronome").Key("bpm").MustInt(120)
    isMetronomeEnabled := cfg.Section("metronome").Key("is_metronome_enabled").MustBool(true)
    soundFile := cfg.Section("metronome").Key("audio_file").MustString("beep.wav")

    fmt.Printf("Configuration loaded:\n")
    fmt.Printf("BPM: %d\n", bpm)
    fmt.Printf("Is Metronome Enabled: %v\n", isMetronomeEnabled)
    fmt.Printf("Sound File: %s\n", soundFile)

    return bpm, isMetronomeEnabled, soundFile
}

func main() {
    bpm, isMetronomeEnabled, soundFile := loadConfig()
    fmt.Println("Starting metronome...")

    // Initialize speaker once
    f, err := os.Open(soundFile)
    if err != nil {
        fmt.Printf("Failed to open sound file: %v\n", err)
        os.Exit(1)
    }
    defer f.Close()

    streamer, format, err := wav.Decode(f)
    if err != nil {
        fmt.Printf("Failed to decode sound file: %v\n", err)
        os.Exit(1)
    }
    defer streamer.Close()

    speaker.Init(format.SampleRate, format.SampleRate.N(time.Second/10))
    runMetronome(bpm, isMetronomeEnabled, soundFile)
}

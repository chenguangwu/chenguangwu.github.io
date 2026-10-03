def main():
    # ---------------- ramp-slope (18) ----------------
    write('ramp-slope', build('ramp-slope', [
        "🗺️ Wheelchair Ramp Slope Calculator",
        "Computes the slope, horizontal length and ramp length of an accessible ramp from the height difference, and checks compliance with the code",
        "Core formulas (by input variable): (horizontal ÷ 100 > 9) || (H > 75 && X <= 12); max(0, Math.ceil(horizontal ÷ 100 ÷ 9) - 1); max(0, Math.ceil(horizontal ÷ 100 ÷ 6) - 1)",
        "📖 Read the \"Wheelchair Ramp Slope Calculator User Guide\"",
        "Slope calculation",
        "Code requirements",
        "📚 Deep dive: Wheelchair Ramp Slope Calculation",
        "Entrance ramp design: height difference 0.40m (40cm), at the general building ratio 1:12, horizontal length=40×12=480cm=4.80m, slant length=√(40²+480²)≈481.7cm≈4.82m, slope≈8.33% (about 4.76°), and the single-run rise of 40cm<75cm is compliant.",
        "Gentle ramp: height difference 0.40m, 1:20, horizontal=800cm=8.00m, slope 5% (about 2.86°), the single-run rise 40cm<120cm is compliant, but the horizontal 8m already approaches the 9m upper limit.",
        "Restricted steep ramp: height difference 0.30m, 1:8 (steepest), horizontal=240cm=2.40m, slope 12.5% (about 7.13°), and the single-run rise 30cm hits the upper limit as a critical case, used only when space is constrained.",
        "Example: height difference 40cm, slope ratio 1:12",
        "Horizontal length L = H×12 = 40×12 = 480cm = 4.80m; slant length = √(40²+480²) = √(1600+230400) = √232000 ≈ 481.66cm ≈ 4.82m; slope = 1/12×100 ≈ 8.33%, angle = atan(40/480) = atan(0.0833) ≈ 4.76°. Code check: X=12 corresponds to a maximum single-run rise of 75cm, and the current 40cm<75cm passes; horizontal 4.80m<9m needs no resting platform.",
        "What is the maximum slope of a wheelchair ramp?",
        "Under GB 55019-2021, a general ramp should not be steeper than 1:12 (about 8.33%); a gentle ramp may use 1:20 (5%); where space is constrained the steepest is 1:8 (12.5%), and the maximum rise of a single run must not exceed 0.30m.",
        "When is a resting platform required?",
        "A resting platform should be provided when the horizontal length of the ramp exceeds 9m or the single-run rise exceeds 0.75m (in the 1:12 case), and the platform depth should not be less than 1.50m; for the 1:10 case, a horizontal length of 6m and a rise of 0.60m likewise requires segmentation and a platform.",
        "About \"Wheelchair Ramp Slope Calculator\"",
        "Wheelchair ramp slope and horizontal projection length calculation, checked against the accessibility design code, with all data processed locally and never uploaded.",
    ]))

    # ---------------- sign-language (17) ----------------
    write('sign-language', build('sign-language', [
        "📖 Sign Language Vocabulary",
        "Chinese Sign Language basic vocabulary with diagrams, including handshape, position and movement description, for learning and communication",
        "📖 Read the \"Sign Language Vocabulary User Guide\"",
        "A quick reference of common sign language vocabulary and signing essentials, assisting communication with hearing-impaired people and sign language learning. Pure front-end local reference, no data uploaded.",
        "📚 Deep dive: Sign Language Vocabulary",
        "Daily communication: look up \"hello\" (one hand in a fist with the thumb moving slightly up / index finger pointing at the other person with a nod), \"thank you\" (thumb bending slightly forward and down from the mouth), \"please\" (palm up, beckoning toward the body), to quickly review common greeting gestures.",
        "Appellation learning: browse the \"appellation\" category to see \"father\" (thumb pulled outward from the corner of the mouth), \"mother\" (little finger pulled outward), \"friend\" (the two index fingers hooked together), distinguishing the common gestures for gendered appellations.",
        "Numeral signs: 1~10 each have a fixed handshape (one = index finger, two = index and middle fingers, ten = both hands crossed into a plus), and in teaching you can drill the signing one by one under the \"numbers\" category.",
        "Example: searching for \"mother\"",
        "Searching \"mother\" among the 43 basic vocabulary items (6 major categories: greetings / appellations / numbers / daily life / emotions / time) matches 1 result: one hand with the little finger extended, pulled outward from the corner of the mouth (the common gesture for female appellation). Filtering by the \"appellation\" category instead shows 8 appellation words (I, you, he/she, father, mother, grandfather, grandmother, friend).",
        "What elements does sign language consist of?",
        "Chinese Sign Language (CSL) consists of handshape, position, orientation, movement and facial expression; the same handshape has different meanings at different positions or orientations; regional habits may vary slightly, so learning is recommended alongside video or a teacher's demonstration.",
        "How many words does this tool include?",
        "43 basic vocabulary items are built in, covering 6 major categories: greetings, appellations, numbers, daily life, emotions and time, with keyword search and category filtering; it serves as a basic reference only, and in-depth expression requires a systematic course and practice.",
        "About \"Sign Language Vocabulary\"",
        "A quick reference of common sign language vocabulary and signing essentials, assisting communication with hearing-impaired people, with all data processed locally and never uploaded.",
        "e.g.: hello, thank you, mother",
    ]))

    # ---------------- voice-synthesis (19) ----------------
    write('voice-synthesis', build('voice-synthesis', [
        "♿ Speech Synthesis",
        "Reads text aloud via the browser Web Speech API, supporting Chinese and English with adjustable rate and pitch",
        "📖 Read the \"Speech Synthesis User Guide\"",
        "Rate (",
        "Pitch (",
        "Volume (",
        "📚 Deep dive: Speech Synthesis",
        "Reading assistance for the visually impaired: paste a long text, select a Chinese voice (zh), and click read; the browser synthesizes the speech locally and reads it character by character, which combined with screen reader software gives accessible reading, and the text is never uploaded to the server.",
        "Chinese / English switching: switch the language filter to English, choose an en voice, and read \"Hello, how are you today?\"; rate and pitch are adjustable (0.5~2.0) to suit different listening preferences.",
        "Public voice announcements: use preset announcements such as \"Please watch your step and proceed slowly.\", adjust the volume / rate to produce waiting-hall and corridor broadcast scripts, and play them on a loop or export them.",
        "Example: reading the default text",
        "The default text \"Welcome to the speech synthesis tool; type here and it will be read aloud.\" (23 characters including punctuation), with a Chinese voice, rate 1.0, pitch 1.0 and volume 1.0 selected; after clicking read the status shows \"Reading… character N\" and updates the character progress in real time via onboundary; when finished it shows \"Reading complete\". The speech is synthesized locally by the browser's built-in engine and requires no network connection.",
        "Does speech synthesis require a network connection?",
        "No. This tool calls the browser's built-in Web Speech API (speechSynthesis) to synthesize speech locally, and the text is not uploaded to the server; the list of available voices differs across browsers and systems, depending on the language packs installed on the machine.",
        "Why can I not hear any sound?",
        "Some browsers only produce sound after the user manually clicks \"read\" (such as the security policy of iOS Safari); if the page reports \"the current browser does not support the Web Speech API\", please switch to the latest Chrome / Edge / Safari.",
        "About \"Speech Synthesis\"",
        "Browser-local text-to-speech (TTS) preview and audition, supporting multiple voices and rate adjustment, with no data uploaded.",
        "Please enter text...",
    ]))


if __name__ == '__main__':
    main()

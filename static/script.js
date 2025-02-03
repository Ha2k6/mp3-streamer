async function fetchStream() {
    const query = document.getElementById("songQuery").value;
    if (!query) {
        alert("Please enter a song name!");
        return;
    }

    try {
        const response = await fetch(`/stream?query=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.stream_url) {
            document.getElementById("audioPlayer").src = data.stream_url;
        } else {
            alert("Song not found!");
        }
    } catch (error) {
        console.error("Error fetching song:", error);
        alert("Failed to fetch the song.");
    }
}
￼Enter

document.getElementById("downloadBtn").addEventListener("click", () => {
  const url = document.getElementById("urlInput").value;
  const quality = document.getElementById("qualitySelect").value;
  const message = document.getElementById("message");

  if (!url) {
    message.textContent = "⚠️ Please enter a YouTube URL.";
    return;
  }

  message.textContent = "⏳ Fetching download link...";

  fetch('/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url, quality: quality })
  })
  .then(response => response.json())
  .then(data => {
    if (data.download_url) {
      message.textContent = "✅ Download starting...";
      const a = document.createElement("a");
      a.href = data.download_url;
      a.download = "";
      a.click();
    } else {
      message.textContent = "⚠️ Error: " + (data.error || "Unknown error.");
    }
  })
  .catch(error => {
    console.error(error);
    message.textContent = "⚠️ Error: Failed to fetch.";
  });
});

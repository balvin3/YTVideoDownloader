document.getElementById("downloadBtn").addEventListener("click", () => {
  const url = document.getElementById("urlInput").value;
  const quality = document.getElementById("qualitySelect").value;
  const message = document.getElementById("message");
  const linkBox = document.getElementById("linkBox");

  message.textContent = "";
  linkBox.innerHTML = "";

  if (!url) {
    message.textContent = "⚠️ Please enter a YouTube URL.";
    return;
  }

  message.textContent = "⏳ Getting download link...";

  fetch('/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, quality })
  })
    .then(response => response.json())
    .then(data => {
      if (data.download_url) {
        message.textContent = "✅ Download link ready:";
        const a = document.createElement("a");
        a.href = data.download_url;
        a.textContent = `⬇️ Download: ${data.title || "Click here"}`;
        a.target = "_blank";
        linkBox.appendChild(a);
      } else {
        message.textContent = "⚠️ Error: " + (data.error || "Unknown error.");
      }
    })
    .catch(error => {
      console.error(error);
      message.textContent = "⚠️ Error: Failed to fetch.";
    });
});

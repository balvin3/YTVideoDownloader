document.getElementById("downloadBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value.trim();
  const quality = document.getElementById("qualitySelect").value;
  const message = document.getElementById("message");
  const linkBox = document.getElementById("linkBox");

  linkBox.innerHTML = "";
  message.textContent = "";

  if (!url) {
    message.textContent = "⚠️ Please enter a YouTube URL.";
    return;
  }

  message.textContent = "⏳ Fetching download link...";

  try {
    const response = await fetch("/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: url, quality: quality })
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Server error (${response.status}): ${errText}`);
    }

    const data = await response.json();

    if (data.error) {
      message.textContent = "⚠️ Error: " + data.error;
      return;
    }

    message.textContent = "✅ Download link ready:";
    linkBox.innerHTML = `
      <p><strong>${data.title}</strong></p>
      <a href="${data.download_url}" target="_blank" rel="noopener noreferrer">⬇️ Download Video</a>
    `;
  } catch (error) {
    console.error("Failed to fetch:", error);
    message.textContent = "⚠️ Failed to fetch: " + error.message;
  }
});

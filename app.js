document.getElementById("downloadBtn").addEventListener("click", async () => {
    const videoUrl = document.getElementById("videoUrl").value.trim();

    if (!videoUrl) {
        alert("⚠️ Shyiramo YouTube link mbere yo gukanda Download.");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: videoUrl })
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Server error (${response.status}): ${errText}`);
        }

        const data = await response.json();

        if (data.error) {
            alert(`⚠️ Error: ${data.error}`);
            return;
        }

        // Show download link
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `
            <p><strong>${data.title}</strong></p>
            <a href="${data.url}" target="_blank">⬇️ Download Video</a>
        `;

    } catch (error) {
        console.error("❌ Failed to fetch:", error);
        alert("❌ Failed to fetch: " + error.message);
    }
});

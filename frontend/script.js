document.addEventListener('DOMContentLoaded', () => {
    // --- Constants and DOM Elements ---
    const API_BASE_URL = 'http://127.0.0.1:8000/api';

    // Main sections
    const uploadSection = document.getElementById('upload-section');
    const resultSection = document.getElementById('result-section');

    // Upload elements
    const uploadButton = document.getElementById('photo-upload-button');
    const uploadInput = document.getElementById('photo-upload-input');

    // Result elements
    const resultImage = document.getElementById('result-image');
    const resultName = document.getElementById('result-name');
    const resultScore = document.getElementById('result-score');
    const resultMeme = document.getElementById('result-meme');
    const tryAgainButton = document.getElementById('try-again-button');

    // UI feedback elements
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const hologramsContainer = document.querySelector('.character-holograms');

    // --- Main Functions ---

    /**
     * Fetches the list of characters from the backend to populate the UI.
     */
    async function fetchCharacters() {
        try {
            const response = await fetch(`${API_BASE_URL}/get-characters`);
            if (!response.ok) {
                throw new Error('Failed to fetch character list.');
            }
            const characters = await response.json();
            populateHolograms(characters);
        } catch (error) {
            console.error('Error fetching characters:', error);
            // Could display a static set of holograms or an error state here
        }
    }

    /**
     * Populates the hologram container with character images.
     * @param {Array<Object>} characters - Array of character objects from the API.
     */
    function populateHolograms(characters) {
        hologramsContainer.innerHTML = ''; // Clear static placeholders
        characters.forEach(character => {
            const panel = document.createElement('div');
            panel.classList.add('hologram-panel');
            // Use a generic class for styling and set the image via style attribute
            panel.style.backgroundImage = `url(${character.image_url})`;
            hologramsContainer.appendChild(panel);
        });
    }

    /**
     * Handles the file selection event.
     */
    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            getMatch(file);
        }
    }

    /**
     * Uploads the image file and fetches the character match.
     * @param {File} file - The image file to upload.
     */
    async function getMatch(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show loading state
        showLoading(true);
        hideError();
        uploadSection.classList.add('hidden');
        hologramsContainer.classList.add('hidden');

        try {
            const response = await fetch(`${API_BASE_URL}/upload-photo`, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                // If response is not OK, the body should contain an `ErrorResponse`
                throw new Error(data.detail || 'An unknown error occurred.');
            }

            displayResult(data);

        } catch (error) {
            displayError(error.message);
        } finally {
            // Hide loading state
            showLoading(false);
        }
    }

    /**
     * Displays the match result on the UI.
     * @param {Object} data - The character match data from the API.
     */
    function displayResult(data) {
        resultImage.src = data.image_url;
        resultName.textContent = data.character_name;
        resultScore.textContent = `${(data.similarity_score * 100).toFixed(2)}%`;
        resultMeme.textContent = `"${data.meme_text}"`;

        uploadSection.classList.add('hidden');
        hologramsContainer.classList.add('hidden');
        resultSection.classList.remove('hidden');
    }

    /**
     * Resets the UI to the initial state.
     */
    function resetUI() {
        resultSection.classList.add('hidden');
        hideError();

        uploadSection.classList.remove('hidden');
        hologramsContainer.classList.remove('hidden');

        // Reset file input to allow uploading the same file again
        uploadInput.value = '';
    }

    // --- UI Helper Functions ---

    function showLoading(isLoading) {
        loadingSpinner.classList.toggle('hidden', !isLoading);
    }

    function displayError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
        // Show the try again button so the user is not stuck
        tryAgainButton.parentElement.parentElement.classList.remove('hidden');
        resultSection.classList.add('hidden');
        uploadSection.classList.add('hidden'); // keep upload hidden on error
    }

    function hideError() {
        errorMessage.classList.add('hidden');
    }

    // --- Event Listeners ---
    uploadButton.addEventListener('click', () => uploadInput.click());
    uploadInput.addEventListener('change', handleFileSelect);
    tryAgainButton.addEventListener('click', resetUI);

    // --- Initial Load ---
    fetchCharacters();
});

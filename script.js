document.addEventListener('DOMContentLoaded', () => {
    const heroSection = document.querySelector('.hero-section');

    // Particle effects
    for (let i = 0; i < 100; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        heroSection.appendChild(particle);
    }

    // Motion streaks
    document.addEventListener('mousemove', (e) => {
        const streak = document.createElement('div');
        streak.classList.add('motion-streak');
        streak.style.left = `${e.pageX}px`;
        streak.style.top = `${e.pageY}px`;
        document.body.appendChild(streak);

        setTimeout(() => {
            streak.remove();
        }, 1000);
    });

    const uploadButton = document.querySelector('.upload-button');
    uploadButton.addEventListener('click', () => {
        // Create a file input element
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';

        // Listen for file selection
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                console.log('File selected:', file.name);
                // Here you would typically handle the file upload,
                // for example, by sending it to a server.
                // For this demo, we'll just log the file name.
                alert(`You have selected: ${file.name}`);
            }
        });

        // Trigger the file input click
        document.body.appendChild(fileInput);
        fileInput.click();
        document.body.removeChild(fileInput);
    });
});

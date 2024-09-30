function openModal(image, title, blurb) {
    
    // Set the modal image and blurb
    document.getElementById('modalImage').src = image.src;
    document.getElementById('imageModalLabel').textContent = title;
    document.getElementById('modalBlurb').textContent = blurb;

    // Show the modal
    var myModal = new bootstrap.Modal(document.getElementById('imageModal'));
    myModal.show();
}

let hidden = true;

function toggleModal() {
    const modal = document.getElementById('modal-background');

    if (visible) {
        modal.classList.add('hidden');
    } else {
        modal.classList.remove('hidden');
    }

    visible = !visible;
}
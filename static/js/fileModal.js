function toggleModal(id) {
    const modal = document.getElementById(id);

    if (modal) {
        modal.toggle();
    } else {
        console.error('Modal element with id ' + id + ' not found');
    }
}
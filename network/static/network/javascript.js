document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.post_edit_button').forEach(element => {
        element.addEventListener('click', event => display(event));
    });
    document.querySelectorAll('.post_edit_save_button').forEach(element => {
        element.addEventListener('click', event => edit_save(event));
    });
    document.querySelectorAll('.image_like_heart').forEach(element => {
        element.addEventListener('click', event => like(event));
    });

    // By default, hide edit
    posts_default();
});

function posts_default() {
    document.querySelectorAll('.listing_posts_js').forEach(element => {
        element.style.display = 'block';
    });
    document.querySelectorAll('.listing_posts_edit_js').forEach(element => {
        element.style.display = 'none';
    });
    document.querySelectorAll('.listing_posts_edit_Message_All').forEach(element => {
        element.style.display = 'none';
    });
}

function display(event) {
    const element = event.target;
    const post_id = element.value;
    element.parentElement.style.display = 'none';
    document.querySelector(`.listing_posts_edit_${post_id}`).style.display = 'block';
}


function edit_save(event) {
    const element = event.target;
    const post_id = element.value;
    const link = element.dataset.path;
    const edited_post_text = document.querySelector(`#listing_posts_textarea_${post_id}`).value;
    const Alert_info = document.querySelector(`#listing_posts_edit_Message_${post_id}`);

    fetch(link, {
        method: 'POST',
        body: JSON.stringify({ newpost_text: edited_post_text }),
    })
        .then(response => response.json())
        .then(result => {
            if (result.success_message) {
                document.querySelector(`#listing_posts_content_${post_id}`).textContent = edited_post_text;
                Alert_info.style.display = 'block';
                Alert_info.innerHTML = result.success_message;
            } else if (result.error) {
                Alert_info.style.display = 'block';
                Alert_info.innerHTML = result.error;
            }
            setTimeout(() => { Alert_info.style.display = 'none'; }, 3000);
            posts_default();
        });
}

function like(event) {
    const element = event.target;
    const post_id = element.value;
    const link = element.dataset.path;

    fetch(link, {
        method: 'POST',
        body: JSON.stringify({ post_id: post_id }),
    })
        .then(response => response.json())
        .then(result => {
            if (result.message === "Success") {
                document.querySelector(`#listing_post_like_${post_id}`).innerHTML = result.likes_num;
            }
        })
        .catch(() => {
            alert("Failed to like the post. Please try again.");
        });
}

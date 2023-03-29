function updateContent(){
    const xhr = new XMLHttpRequest();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log(csrftoken)
    const inputReview = document.getElementById("reviewInput");
    console.log(inputReview.value)
    const jsonData = {
        "inputReview":
        inputReview.value,
    };


    xhr.onreadystatechange = function (){
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.responseText);
            const response = JSON.parse(this.responseText);
            console.log(response);
            document.querySelector('#content').innerHTML = response.content;
        }
    };
    xhr.open('POST', 'jstest');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xhr.send(JSON.stringify(jsonData));
}
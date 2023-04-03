// 发出请求
// 请求内容:
// 1. input中的review
// 2. 中英文
// 3. 按钮的内容
// 4. 分页的问题？ 要判断输入的餐馆还是物品还是商品描述
// 5. 1-5星

function updateContent(){
    const xhr = new XMLHttpRequest();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log(csrftoken)
    // get textarea input
    const inputReview = document.getElementById("reviewInput");

    // get input language
    const inputLanguageButtons = document.getElementsByName("selectLanguage");
    let selectedLanguage = null;
    for (let i=0; i<inputLanguageButtons.length; i++){
        if (inputLanguageButtons[i].checked) {
            selectedLanguage = inputLanguageButtons[i].value;
            console.log(selectedLanguage);
        }
    }

    // get input function
    const inputApplication = document.getElementsByName("application");
    let selectedApplication = null;
    for (let i=0; i<inputApplication.length; i++){
        if (inputApplication[i].checked) {
            selectedApplication = inputApplication[i].value;
            console.log(selectedApplication);
        }
    }

    // get input keywords
    const inputKeyWords = document.getElementsByName("keyWords")
    const selectedKeyWords = [];
    for (let i=0; i<inputKeyWords.length; i++){
        if (inputKeyWords[i].checked){
            selectedKeyWords.push(inputKeyWords[i].value);
        }
    }
    console.log(selectedKeyWords);


    // get star rating
    const inputRate = document.getElementsByName("rate");
    let selectedRate = null;
    for (let i=0; i<inputRate.length; i++){
        if (inputRate[i].checked) {
            selectedRate = inputRate[i].value;
            console.log(selectedRate);
        }
    }

    const jsonData = {
        "inputReview":
        inputReview.value,
        "selectedLanguage":
        selectedLanguage,
        "selectedApplication":
        selectedApplication,
        "selectedRate":
        selectedRate,
        "selectedKeyWords":
        selectedKeyWords,

    };


    xhr.onreadystatechange = function (){
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.responseText);
            const response = JSON.parse(this.responseText);
            console.log(response);
            // document.querySelector('#content').innerHTML = response.content;
            document.querySelector('#content').innerHTML = "<p>your inputReview: " + response.inputReview + "\n</p>"
                                                                    + "<p>your selectedLanguage: " + response.selectedLanguage + "\n</p>"
                                                                    + "<p>your selectedApplication: " + response.selectedApplication + "\n</p>"
                                                                    + "<p>your selectedRate: " + response.selectedRate + "\n</p>"
                                                                    + "<p>your selectedKeyWords: " + response.selectedKeyWords + "\n</p>";
        }
    };
    xhr.open('POST', 'jstest');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xhr.send(JSON.stringify(jsonData));
}
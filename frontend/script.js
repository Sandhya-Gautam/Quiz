
const score_sec = document.getElementById('score');


async function getQuestion() {
    const url = 'http://127.0.0.1:8000/app/get_question/';
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Token 18f1a487fbd3a79af99897a421143e34a76eca9d`
            }
        });
        if (!response.ok) {
            throw Error(response.statusText);

        }
        const data = await response.json();
        console.log(data);
        return data;
    }
    catch (error) {
        console.log(error);
    }

}

async function startGame() {
    const questionSec = document.getElementById('questionSec');
    const optionSec = document.getElementById('answerOption');
    const content = document.getElementById('content')
    const playground = document.getElementById('playground')
    questionSec.innerHTML = ``;
    optionSec.innerHTML = ``;
    content.style.display ="none";
    playground.style.display ="block";
    const data=await getQuestion();
    console.log(data);
    const question= data.question;
    const answers= data.answers;
    questionSec.innerHTML=`<h1>${question}</h1>`;
    for (let i=0; i<answers.length; i++){
        optionSec.innerHTML += `<li onclick="checkAnswer(${answers[i].label}, ${ answers[i].id })">${answers[i].answer}</li>`;
    }
    
}

function checkAnswer( answerLabel, answerID ) {
    updateScore(answerID);
    startGame();
    playground = document.getElementsByClassName("playground")
    if (answerLabel){
        right_score += 1;
    }
    else {
        wrong_score += 1;
    }
    score_sec.innerHTML = `<span>Right: ${right_score}<span><span> Wrong: ${wrong_score} <span>`;
    // startGame();
}

async function updateScore(id) {
    console.log(id);
    const url = "http://127.0.0.1:8000/app/check_answer/";
    try {
        const response = await fetch(url, {
            method: 'PUT',
            body: JSON.stringify({ "id": id }),
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Token 18f1a487fbd3a79af99897a421143e34a76eca9d`
            }
        });
        if (!response.ok) {
            console.log(response);
            throw Error(response.statusText);

        }
        const data = await response.json();
        console.log(data);
    }
    catch (error) {
        console.log(error);
    }
}

async function getScore() {
    const url = 'http://127.0.0.1:8000/app/get_score/';
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Token 18f1a487fbd3a79af99897a421143e34a76eca9d`
            }
        });
        if (!response.ok) {
            throw Error(response.statusText);

        }
        // console.log(response);
        const data = await response.json();
        // console.log(data);
        right_score=data.right_count;
        wrong_score=data.wrong_count;
        score_sec.innerHTML = `<span>Right: ${right_score}<span><span> Wrong: ${wrong_score} <span>`;

    }       
    catch (error) {
        console.log(error);
    }
}


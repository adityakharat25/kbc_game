let questionIndex = 0;
let idx = 0;
let selectedOption = null;
let timer;
let timeLeft = 45;
let currentPrizeIndex = 14; // Start from the bottom (1,000)
let questions = [];
let cur = 0;
let safe = '0';
// let flip = 0;
// Lifeline usage tracking
let lifelinesUsed = {
  fiftyFifty: false,
  audiencePoll: false,
  askExpert: false,
  flip: false
};

// Fetch questions when page loads
window.onload = function () {
  fetchQuestions();
};

function fetchQuestions() {
  fetch('/get_all_questions')
    .then(response => response.json())
    .then(data => {
      questions = data;
      loadQuestion();
    })
    .catch(error => {
      console.error('Error fetching questions:', error);
      // Fallback questions if fetch fails
      questions = [
      {
          "question": "Which country is known as the 'Land of the Rising Sun'?",
          "options": ["China", "Japan", "Thailand", "South Korea"],
          "answer": "Japan"
      },
      {
          "question": "Who wrote the Indian National Anthem?",
          "options": ["Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Subhash Chandra Bose"],
          "answer": "Rabindranath Tagore"
      },
      {
          "question": "Who painted the Mona Lisa?",
          "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
          "answer": "Leonardo da Vinci"
      },
      {
          "question": "Who invented the telephone?",
          "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Guglielmo Marconi"],
          "answer": "Alexander Graham Bell"
      },
      {
          "question": "How would one say goodbye in Spanish?",
          "options": ["Hola", "Au Revoir", "Salir", "Adiós"],
          "answer": "Adiós"
      },
       {
          "question": "What does VR stand for?",
          "options": ["Very Real", "Visual Recognition", "Voice Recognition", "Virtual Reality"],
          "answer": "Virtual Reality"
      },
      {
          "question": "How many Harry Potter books are there?",
          "options": ["8", "5", "6", "7"],
          "answer": "7"
      },
      {
          "question": "What is the unit of electrical resistance?",
          "options": ["Mho", "Tesla", "Joule", "Ohm"],
          "answer": "Ohm"
      },
      {
          "question": "Who plays protagonist Ethan Hunt in the 'Mission: Impossible' film series?",
          "options": ["Johnny Depp", "Sean Connery", "Pierce Brosnan", "Tom Cruise"],
          "answer": "Tom Cruise"
      },
      {
          "question": "Which UK country features a dragon on their flag?",
          "options": ["England", "North Ireland", "Scotland", "Wales"],
          "answer": "Wales"
      },
      {
          "question": "Kuala Lumpur is the capital of which country?",
          "options": ["Indonesia", "Singapore", "Thailand", "Malaysia"],
          "answer": "Malaysia"
      },
      {
          "question": "Which of these is NOT a city in India?",
          "options": ["Noida", "Ahmedabad", "Ghaziabad", "Islamabad"],
          "answer": "Islamabad"
      },
      {
          "question": "In which country was the Statue of Liberty built and exported to the United States of America?",
          "options": ["Germany", "Spain", "England", "France"],
          "answer": "France"
      },
      {
          "question": "What was the first sport to have been played on the moon?",
          "options": ["Football", "Tennis", "Soccer", "Golf"],
          "answer": "Golf"
      },
      {
          "question": "Which of these games includes the phrase 'Do not pass Go, do not collect $200'?",
          "options": ["Pay Day", "Cluedo", "Coppit", "Monopoly"],
          "answer": "Monopoly"
      },
      {
          "question": "Where are the cars of the brand Ferrari manufactured?",
          "options": ["Romania", "Germany", "Russia", "Italy"],
          "answer": "Italy"
      },
      {
          "question": "How many time zones does China have?",
          "options": ["3", "4", "2", "1"],
          "answer": "1"
      }
      ];
      loadQuestion();
    });
}

function loadQuestion() {
  if (currentPrizeIndex < 0) {
    document.getElementById("question").innerText = "Congratulations! You won 1 Crore !!";
    document.getElementById("options").innerHTML = "";
    clearInterval(timer);
    return;
  }
  idx=questionIndex+Math.floor(Math.random() * 7);
  const currentQuestion = questions[idx];
  document.getElementById("question").innerText = currentQuestion.question;
  selectedOption = null;
  let optionsHTML = "";
  let ch = 'A';
  let chans = 'A';
  currentQuestion.options.forEach((option, index) => {
    if (option == currentQuestion.answer) {
      chans = ch;
    }
    ch = String.fromCharCode(ch.charCodeAt(0) + 1);
  });
  currentQuestion.answer = chans + " : " + currentQuestion.answer;
  ch = 'A';
  currentQuestion.options.forEach((option, index) => {
    option = ch + " : " + option;
    optionsHTML += `<button class="option" onclick="selectOption(this, '${option}', '${currentQuestion.answer}')">${option}</button>`;
    ch = String.fromCharCode(ch.charCodeAt(0) + 1);
  });

  document.getElementById("options").innerHTML = optionsHTML;

  // Update prize highlight
  updatePrizeHighlight();

  // Reset timer
  resetTimer();
}

function selectOption(button, selected, correctAnswer) {
  // Clear previous selections
  document.querySelectorAll(".option").forEach(btn => {
    btn.classList.remove("selected");
  });

  // Highlight selected option
  button.classList.add("selected");
  selectedOption = { button, selected, correctAnswer };
}
function strToint(str) {
  return parseInt(str.replace(/,/g, ''), 10);
}
function lockAnswer() {
  if (!selectedOption) {
    alert("Please select an option first!");
    return;
  }

  clearInterval(timer);

  if (selectedOption.selected === selectedOption.correctAnswer) {
    selectedOption.button.classList.add("correct");
    let pre = document.querySelectorAll(".prize")[currentPrizeIndex].innerText;
    cur = strToint(pre);
    if (pre == "10,000") {
      safe = "10,000";
    }
    if (pre == "3,20,000") {
      safe = "3,20,000";
    }
    // Move to next question after a delay
    setTimeout(() => {
      questionIndex += 7;
      currentPrizeIndex--;
      loadQuestion();
    }, 1000);
  } else {
    selectedOption.button.classList.add("wrong");

    // Show game over after a delay
    setTimeout(() => {
      if (safe == '0') {
        document.getElementById("question").innerText = `Wrong answer! Game Over!\nYou have won nothing`;
        document.getElementById("options").innerHTML = "";
        clearInterval(timer);
        disableAllButtons();
        disableAllLifelines();
        return;
      }
      else {
        document.getElementById("question").innerText = `Wrong answer! Game Over!\nYou have won : ${safe}`;
        document.getElementById("options").innerHTML = "";
        clearInterval(timer);
        disableAllButtons();
        disableAllLifelines();
        return;
        // alert(`Wrong answer! Game Over!\nYou have own : ${safe}`);
      }
      // resetGame();
    }, 1500);
  }
}

function quitGame() {
  const dialog = document.getElementById("quitDialog");
  dialog.showModal();

  document.getElementById("confirmQuit").addEventListener("click", () => {
    dialog.close();

    // Display the quit message
    document.getElementById("question").innerText = `Game Over!\nYou have won: ${cur}`;
    document.getElementById("options").innerHTML = "";

    // Disable all buttons
    disableAllButtons();
    disableAllLifelines();
    clearInterval(timer);
  });

  document.getElementById("cancelQuit").addEventListener("click", () => {
    dialog.close();
  });
}

// Function to disable all buttons
function disableAllButtons() {
  const buttons = document.querySelectorAll("button");
  buttons.forEach(button => {
    button.disabled = true;
  });
}

function disableAllLifelines() {
  const lifelines = document.querySelectorAll(".lifeline");
  lifelines.forEach(lifeline => {
      lifeline.style.pointerEvents = "none";  // Disables clicking
      lifeline.style.opacity = "0.5";  // Makes it look disabled
  });
}
function enableAllLifelines() {
  const lifelines = document.querySelectorAll(".lifeline");
  lifelines.forEach(lifeline => {
      lifeline.style.pointerEvents = "auto"; // Enables clicking
      lifeline.style.opacity = "1"; // Restores full visibility
  });
}

function resetGame() {
  questionIndex = 0;
  selectedOption = null;
  timeLeft = 45;
  currentPrizeIndex = 14; // Start from the bottom (1,000)
  cur = 0;
  safe = '0';

  // Reset lifeline usage tracking
  lifelinesUsed = {
    fiftyFifty: false,
    audiencePoll: false,
    askExpert: false,
    flip: false
  };

  // Re-enable all buttons
  enableAllButtons();
  enableAllLifelines();
  // Reset lifeline visuals
  document.querySelectorAll(".lifeline").forEach(lifeline => {
    lifeline.classList.remove("used");
  });

  loadQuestion();
}

// Function to enable all buttons
function enableAllButtons() {
  const buttons = document.querySelectorAll("button");
  buttons.forEach(button => {
    button.disabled = false;
  });
}


function resetTimer() {
  clearInterval(timer);
  timeLeft = 45;
  document.getElementById("clock").innerText = timeLeft;

  timer = setInterval(() => {
    timeLeft--;
    document.getElementById("clock").innerText = timeLeft;

    if (timeLeft <= 1) {
      setTimeout(() => {
        if (safe == '0') {
          document.getElementById("question").innerText = `Time UP! Game Over!\nYou have won nothing`;
          document.getElementById("options").innerHTML = "";
          clearInterval(timer);
          disableAllButtons();
          disableAllLifelines();
          return;
        }
        else {
          document.getElementById("question").innerText = `Time UP! Game Over!\nYou have won : ${safe}`;
          document.getElementById("options").innerHTML = "";
          clearInterval(timer);
          disableAllButtons();
          disableAllLifelines();
          return;
        }
      }, 1500);
    }
  }, 1000);
}

function updatePrizeHighlight() {
  const prizes = document.querySelectorAll(".prize");
  prizes.forEach((prize, index) => {
    prize.classList.remove("active", "won");
    if (index > currentPrizeIndex) {
      prize.classList.add("won"); // Mark previous prizes as won (green)
    }
  });

  prizes[currentPrizeIndex].classList.add("active");
}

// Lifeline functions
function useFiftyFifty() {
  if (lifelinesUsed.fiftyFifty || !questions[idx]) return;

  document.getElementById("fifty-fifty").classList.add("used");
  lifelinesUsed.fiftyFifty = true;

  const correctAnswer = questions[idx].answer;
  const options = document.querySelectorAll(".option");

  // Count incorrect options that we'll hide
  let incorrectToHide = 2;
  let visibleIncorrect = 0;

  // Randomly hide 2 incorrect options
  for (let i = 0; i < options.length; i++) {
    if (options[i].innerText !== correctAnswer && incorrectToHide > 0) {
      options[i].style.visibility = "hidden";
      incorrectToHide--;
    } else if (options[i].innerText !== correctAnswer) {
      visibleIncorrect++;
    }
  }
}

function useAudiencePoll() {
  if (lifelinesUsed.audiencePoll || !questions[idx]) return;

  document.getElementById("audience-poll").classList.add("used");
  lifelinesUsed.audiencePoll = true;

  const correctAnswer = questions[idx].answer;
  const options = document.querySelectorAll(".option");

  let results = [
    { option: "A", percentage: 0 },
    { option: "B", percentage: 0 },
    { option: "C", percentage: 0 },
    { option: "D", percentage: 0 }
  ];

  let remainingOptions = Array.from(options).filter(option => option.style.visibility !== "hidden"); // Only visible options

  if (remainingOptions.length === 2) {
    // 50-50 case (one correct, one incorrect)
    const correctPercentage = Math.floor(Math.random() * 31) + 60; // Between 60% - 90%
    const incorrectPercentage = 100 - correctPercentage;

    remainingOptions.forEach(option => {
      const optionLetter = option.innerText[0];
      if (option.innerText === correctAnswer) {
        results["ABCD".indexOf(optionLetter)].percentage = correctPercentage;
      } else {
        results["ABCD".indexOf(optionLetter)].percentage = incorrectPercentage;
      }
    });

  } else {
    // Normal case (4 options)
    let allocatedPercentage = 0;
    let correctPercentage = Math.floor(Math.random() * 31) + 50; // Between 50% - 80%
    let remainingPercentage = 100 - correctPercentage;

    results["ABCD".indexOf(correctAnswer[0])].percentage = correctPercentage;

    let incorrectOptions = results.filter(r => r.option !== correctAnswer[0]);

    for (let i = 0; i < incorrectOptions.length; i++) {
      let randomPercentage = i === incorrectOptions.length - 1
        ? remainingPercentage - allocatedPercentage
        : Math.floor(Math.random() * (remainingPercentage - allocatedPercentage));

      results["ABCD".indexOf(incorrectOptions[i].option)].percentage = randomPercentage;
      allocatedPercentage += randomPercentage;
    }
  }

  // Display the graph
  showAudiencePollGraph(results);
}


function showAudiencePollGraph(results) {
  const dialog = document.getElementById("audiencePollDialog");
  const ctx = document.getElementById("pollChart").getContext("2d");

  if (window.pollChartInstance) {
    window.pollChartInstance.destroy(); // Destroy previous chart instance
  }

  window.pollChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: results.map(r => r.option),
      datasets: [{
        label: "Audience Votes",
        data: results.map(r => r.percentage),
        backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0"],
        borderColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0"],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: function (value) {
              return value + "%";
            }
          }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.parsed.y + "%";
            }
          }
        }
      }
    }
  });

  dialog.showModal();

  dialog.querySelector(".close-dialog").addEventListener("click", () => {
    dialog.close();
  });
}


function useAskExpert() {
  if (lifelinesUsed.askExpert || !questions[idx]) return;
  document.getElementById("ask-expert").classList.add("used");
  lifelinesUsed.askExpert = true;
  const correctAnswer = questions[idx].answer;

  const dialog = document.getElementById("askExpertDialog");
  const expertAnswer = document.getElementById("expertAnswer");

  // 95% chance the expert is correct
  if (Math.random() < 0.95) {
    expertAnswer.textContent = `I believe the correct answer is "${correctAnswer}".`;
  } else {
    // Expert gives wrong answer
    const options = questions[questionIndex].options.filter(option => option !== correctAnswer);
    const wrongAnswer = options[Math.floor(Math.random() * options.length)];
    expertAnswer.textContent = `I think the answer might be "${wrongAnswer}".`;
  }

  dialog.showModal();

  dialog.querySelector('.close-dialog').addEventListener('click', () => {
    dialog.close();
  });
}


function useFlip() {
  if (lifelinesUsed.flip || !questions[idx]) return;

  document.getElementById("flip").classList.add("used");
  lifelinesUsed.flip = true;

  // Skip current question
  questionIndex++;
  loadQuestion();
}

module.exports = { strToint, updatePrizeHighlight, resetGame, prizes, currentPrizeIndex };
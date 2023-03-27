function checkAnswer() {
  // Get the selected answer
  var selectedAnswer = document.querySelector('input[name="question_answer"]:checked');
  if (selectedAnswer === null) {
    // No answer selected
    document.getElementById("response_message").innerHTML = "Please select an answer.";
  } else {
    // Submit the form
    document.getElementById("answer-form").submit();
    // Hide footbar
    document.getElementById("footbar_correct").style.display = "none";
    document.getElementById("footbar_wrong").style.display = "none";
  }
}

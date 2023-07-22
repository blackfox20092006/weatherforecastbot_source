var speechOn = false;

function scrollModuleToBottom() {
  var chatModule = document.querySelector('.chat-module');
  chatModule.scrollTop = chatModule.scrollHeight;
}

function sendInput() {
  var inputElt = document.querySelector('[data-role="user-input"]');
  if (inputElt.value == '') return;
  toggleInput(false);
  var thread = document.querySelector('.thread');
  var newThreadItem = createThreadItem(false);
  var responseItem = newThreadItem.querySelector('.response');
  responseItem.innerHTML = "Bạn : " + inputElt.value;
  var data = inputElt.value;
  thread.appendChild(newThreadItem);
  inputElt.value = '';
  scrollModuleToBottom();
  setTimeout(function () {
    showResponse(data);
  }, 200);
}


function createThreadItem(isBot) {
  var thread = document.querySelector('.thread');
  var threadItem = document.createElement('div');
  var avatarItem = document.createElement('div');
  var responseContainerItem = document.createElement('div');
  var responseItem = document.createElement('div');
  threadItem.classList.add('thread-item');
  avatarItem.classList.add('avatar-container');
  responseContainerItem.classList.add('response-container');
  responseItem.classList.add('response');
  responseContainerItem.appendChild(responseItem);
  threadItem.appendChild(avatarItem);
  threadItem.appendChild(responseContainerItem);
  thread.appendChild(threadItem);
  if (isBot) {
    avatarItem.appendChild(createBotAvatar());
  } else {
    threadItem.classList.add('user-item');
  }
  return threadItem;
}

function createBotAvatar() {
  // make previous avatar inactive
  var previousAvatar = document.querySelector('.calliope.idle:not(.big), .calliope.appearing:not(.big)');
  if (previousAvatar) {
    previousAvatar.classList.remove('idle');
    previousAvatar.classList.remove('appearing');
    previousAvatar.classList.add('inactive');
  }
  var calliopeItem = document.createElement('div');
  var headItem = document.createElement('div');
  var eyeLeftItem = document.createElement('div');
  var eyeRightItem = document.createElement('div');
  var torsoItem = document.createElement('div');
  var armLeftItem = document.createElement('div');
  var armRightItem = document.createElement('div');
  var feetItem = document.createElement('div');
  calliopeItem.classList.add('calliope');
  calliopeItem.classList.add('appearing');
  headItem.classList.add('head');
  eyeLeftItem.classList.add('eye-left');
  eyeRightItem.classList.add('eye-right');
  torsoItem.classList.add('torso');
  armLeftItem.classList.add('arm-left');
  armRightItem.classList.add('arm-right');
  feetItem.classList.add('feet');
  headItem.appendChild(eyeLeftItem);
  headItem.appendChild(eyeRightItem);
  torsoItem.appendChild(armLeftItem);
  torsoItem.appendChild(armRightItem);
  calliopeItem.appendChild(headItem);
  calliopeItem.appendChild(torsoItem);
  calliopeItem.appendChild(feetItem);
  return calliopeItem;
}

function showResponse(question) {
  var thread = document.querySelector('.thread');
  var newThreadItem = createThreadItem(true);
  var responseItem = newThreadItem.querySelector('.response');
  thread.appendChild(newThreadItem);

  var encodedQuestion = encodeURIComponent(question);
  var url = 'http://127.0.0.1:5000/get_answer?question=' + encodedQuestion;

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var responseJSON = JSON.parse(xhr.responseText);
        var answer = responseJSON.answer;

        if (isWeatherQuestion(question)) {
          var weatherInfo = responseJSON.answer;
          var weatherAnswer = "Bot: Đã tìm thấy thông tin!!" + "<br>"
            + "*****************Hôm nay***************** " + "<br>"
            + "Địa điểm: " + weatherInfo.name + "<br>"
            + "Nhiệt độ hiện tại : " + weatherInfo.temperature + "<br>"
            + "Tình trạng thời tiết hiện tại : " + weatherInfo.condition + "<br>"
            + "Bạn sẽ cảm thấy : " + weatherInfo.feel_like + "°C" + "<br>"
            + "****************************************" + "<br>"
            + "Ngày: " + weatherInfo.date + "<br>"
            + "Nhiệt độ cao nhất: " + weatherInfo.max_temp + "°C" + "<br>"
            + "Nhiệt độ thấp nhất: " + weatherInfo.min_temp + "°C" + "<br>"
            + "Tình trạng thời tiết: " + weatherInfo.condition;

          responseItem.innerHTML = weatherAnswer;
          // Hiển thị thông tin thời tiết trên website
          showWeatherInfo(weatherAnswer);
        } else {
          responseItem.innerHTML = "BF: " + answer;
          // Xóa thông tin thời tiết trên website
          clearWeatherInfo();
        }

        scrollModuleToBottom();
        toggleInput(true);
      } else {
        console.error('Đã xảy ra lỗi khi gọi API');
      }
    }
  };

  xhr.send();
}

function isWeatherQuestion(question) {
  // Kiểm tra nếu câu hỏi là dự báo thời tiết
  return question.startsWith("dubaothoitiet");
}

function showWeatherInfo(answer) {
  var weatherInfoElement = document.querySelector('.weather-info');
  if (weatherInfoElement) {
    weatherInfoElement.innerHTML = answer;
  }
}

function clearWeatherInfo() {
  var weatherInfoElement = document.querySelector('.weather-info');
  if (weatherInfoElement) {
    weatherInfoElement.innerHTML = '';
  }
}

function manageChatOverlay() {
  var overlay = document.querySelector('.scroll-overlay');
  var chatModule = document.querySelector('.chat-module');
  if (chatModule.scrollTop > 0) {
    overlay.classList.remove('overlay-hidden');
  } else {
    overlay.classList.add('overlay-hidden');
  }
}

function toggleInput(enabled) {
  var inputElement = document.querySelector('[data-role="user-input"]');
  inputElement.disabled = !enabled;
  if (enabled) {
    inputElement.focus();
  }
}
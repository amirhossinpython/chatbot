$(document).ready(function () {
    // باز کردن منو
    $("#openMenu").click(function () {
        $("#sidebar").addClass("active");
    });

    // بستن منو
    $("#closeMenu").click(function () {
        $("#sidebar").removeClass("active");
    });

    // ارسال پیام با کلیک روی دکمه
    $("#sendMessage").click(function () {
        sendMessage();
    });

    // ارسال پیام با فشردن کلید Enter
    $("#userMessage").keypress(function (event) {
        if (event.which === 13) {
            sendMessage();
        }
    });

    // ارسال پیام به سرور و نمایش در چت‌باکس
    function sendMessage() {
        const message = $("#userMessage").val().trim();
        if (message !== "") {
            addMessageToChat(message, "user");

            // نمایش وضعیت در حال پردازش
            $("#processing").show();

            // ارسال پیام به سرور
            $.ajax({
                url: "/chat",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ message: message }),
                success: function (response) {
                    $("#processing").hide();
                    addMessageToChat(response.response_message, "bot");
                },
                error: function () {
                    $("#processing").hide();
                    addMessageToChat("خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.", "bot");
                }
            });

            $("#userMessage").val("");
        }
    }

    // افزودن پیام به چت‌باکس
    function addMessageToChat(message, sender) {
        const chatBox = $("#chatBox");
        const messageElement = $("<p></p>").text(message).addClass(sender);
        chatBox.append(messageElement);
        chatBox.scrollTop(chatBox[0].scrollHeight);
    }
});

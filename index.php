<?php
$sentences = [
    "Я люблю программировать на Python",
    "Сегодня хорошая погода",
    "Telegram боты это удобно",
    "Сложные капчи это интересно"
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Проверка капчи
    $user_answer = $_POST['captcha'];
    $correct_sentence = $_POST['correct_sentence'];

    if ($user_answer == $correct_sentence) {
        $user_id = rand(1000, 9999);  // Генерация случайного ID
        $password = bin2hex(random_bytes(4));  // Генерация случайного пароля

        // Отправка данных на сервер
        $data = [
            'user_id' => $user_id,
            'password' => $password
        ];

        $options = [
            'http' => [
                'header'  => "Content-type: application/json\r\n",
                'method'  => 'POST',
                'content' => json_encode($data),
            ],
        ];

        $context  = stream_context_create($options);
        $result = file_get_contents('http://localhost:5000/register', false, $context);

        if ($result !== FALSE) {
            echo "Регистрация успешна!<br>";
            echo "Ваш ID: $user_id<br>";
            echo "Ваш пароль: $password";
        } else {
            echo "Ошибка регистрации. Попробуйте позже.";
        }
    } else {
        echo "Неверный ответ. Попробуйте еще раз.";
    }
} else {
    // Генерация капчи
    $sentence = $sentences[array_rand($sentences)];
    $words = explode(' ', $sentence);
    shuffle($words);
    $shuffled_sentence = implode(' ', $words);

    // Форма с капчей
    echo '
    <form method="POST">
        <label for="captcha">Расставь слова в правильном порядке:</label><br>
        <strong>' . htmlspecialchars($shuffled_sentence) . '</strong><br>
        <input type="text" id="captcha" name="captcha"><br>
        <input type="hidden" name="correct_sentence" value="' . htmlspecialchars($sentence) . '">
        <button type="submit">Отправить</button>
    </form>
    ';
}
?>
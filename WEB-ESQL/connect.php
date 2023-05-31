<!DOCTYPE html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>MySql-PHP 연결 테스트</title>
</head>
<body>
<?php
    $servername = "localhost";
    $user = "root";
    $password = "Min02choi!";
 
    $connect = mysqli_connect($servername, $user, $password);
    if (!$connect) {
        die("서버와의 연결 실패! : ".mysqli_connect_error());
    }
    echo "서버와의 연결 성공!";
?>
</body>
</html>
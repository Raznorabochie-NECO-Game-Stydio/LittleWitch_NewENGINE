<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Little Witch - Игровая Студия</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #f0f0f0;
            min-height: 100vh;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        
        .rounded-gif {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            margin: 30px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 3px solid #6a3093;
        }
        
        .rounded-gif:hover {
            transform: scale(1.02);
            box-shadow: 0 15px 40px rgba(106, 48, 147, 0.4);
        }
        
        .rounded-gif img {
            display: block;
            width: 100%;
            height: auto;
            max-width: 600px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: 3.5rem;
            margin: 20px 0;
            background: linear-gradient(45deg, #a166ab, #6a3093, #a166ab);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 2px 10px rgba(106, 48, 147, 0.3);
        }
        
        .subtitle {
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: #c4c4c4;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }
        
        .buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }
        
        .btn {
            padding: 12px 30px;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #6a3093, #a166ab);
            color: white;
            box-shadow: 0 4px 15px rgba(106, 48, 147, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(106, 48, 147, 0.6);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: #f0f0f0;
            border: 1px solid #6a3093;
        }
        
        .btn-secondary:hover {
            background: rgba(106, 48, 147, 0.2);
            transform: translateY(-3px);
        }
        
        .features {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin: 40px 0;
        }
        
        .feature {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            width: 220px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateY(-5px);
            background: rgba(106, 48, 147, 0.1);
        }
        
        .feature i {
            font-size: 2rem;
            color: #a166ab;
            margin-bottom: 15px;
        }
        
        .feature h3 {
            margin-bottom: 10px;
            color: #e0e0e0;
        }
        
        .feature p {
            font-size: 0.9rem;
            color: #b0b0b0;
        }
        
        .footer {
            margin-top: 40px;
            color: #888;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2.5rem;
            }
            
            .buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .features {
                flex-direction: column;
                align-items: center;
            }
            
            .feature {
                width: 100%;
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="rounded-gif">
            <img src="https://github.com/Raznorabochie-NECO-Game-Stydio/LittleWitch_NewENGINE/raw/master/main_menu.gif" alt="Главное меню Little Witch">
        </div>
        
        <h1>Little Witch</h1>
        
        <p class="subtitle">
            Окунитесь в магический мир приключений с Little Witch - захватывающей игрой, 
            где вы играете за юную ведьму, открывающую тайны древнего мира.
        </p>
        
        <div class="buttons">
            <a href="#" class="btn btn-primary">Играть сейчас</a>
            <a href="#" class="btn btn-secondary">Узнать больше</a>
        </div>
        
        <div class="features">
            <div class="feature">
                <i>✨</i>
                <h3>Магия и заклинания</h3>
                <p>Изучайте мощные заклинания и улучшайте свои магические навыки</p>
            </div>
            <div class="feature">
                <i>🌍</i>
                <h3>Открытый мир</h3>
                <p>Исследуйте огромный мир, полный тайн и приключений</p>
            </div>
            <div class="feature">
                <i>🎮</i>
                <h3>Увлекательный геймплей</h3>
                <p>Решайте головоломки, сражайтесь с врагами и находите союзников</p>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2023 Raznorabochie NECO Game Studio. Все права защищены.</p>
        </div>
    </div>
</body>
</html>

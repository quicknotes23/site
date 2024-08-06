document.addEventListener("DOMContentLoaded", function() {
    let slideIndex = 1;
    const totalSlides = 3; // Número total de slides

    function showSlides(n) {
        let slides = document.getElementsByClassName("mySlides");

        // Ajusta o índice do slide
        if (n > totalSlides) { slideIndex = 1; }
        if (n < 1) { slideIndex = totalSlides; }

        // Oculta todos os slides
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";  
        }

        // Exibe o slide atual
        slides[slideIndex - 1].style.display = "block";  
    }

    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    // Inicializa o slideshow
    showSlides(slideIndex);

    // Expondo as funções para navegação manual
    window.plusSlides = plusSlides;

    // Configuração para troca automática de slides
    setInterval(function() {
        plusSlides(1);
    }, 9000); // Muda a imagem a cada 9 segundos

    // Atualiza os slides ao redimensionar a tela
    window.addEventListener('resize', function() {
        showSlides(slideIndex);
    });
});


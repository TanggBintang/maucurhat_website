// Inisialisasi AOS (Animate on Scroll)
document.addEventListener('DOMContentLoaded', function() {
    // Inisialisasi AOS
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true
    });
    
    // Menghilangkan pesan flash secara otomatis setelah 5 detik
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Toggle mode gelap
    const toggleDarkMode = document.getElementById('toggleDarkMode');
    if (toggleDarkMode) {
        toggleDarkMode.addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('dark-mode');
            
            // Ganti ikon bulan/matahari
            const icon = this.querySelector('i');
            if (document.body.classList.contains('dark-mode')) {
                icon.classList.remove('bi-moon-fill');
                icon.classList.add('bi-sun-fill');
                localStorage.setItem('darkMode', 'enabled');
            } else {
                icon.classList.remove('bi-sun-fill');
                icon.classList.add('bi-moon-fill');
                localStorage.setItem('darkMode', 'disabled');
            }
        });
        
        // Cek preferensi mode dari localStorage
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark-mode');
            const icon = toggleDarkMode.querySelector('i');
            icon.classList.remove('bi-moon-fill');
            icon.classList.add('bi-sun-fill');
        }
    }
    
    // Animasi pada scroll
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            nav.style.padding = '10px 0';
        } else {
            nav.style.padding = '15px 0';
        }
    });
    
    // Efek ripple pada tombol
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.offsetLeft;
            const y = e.clientY - e.target.offsetTop;
            
            const ripple = document.createElement('span');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            this.appendChild(ripple);
            
            setTimeout(function() {
                ripple.remove();
            }, 600);
        });
    });
    
    // Efek hover pada kartu curhatan
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Validasi form sederhana
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Tambahkan pesan error jika belum ada
                    const nextElement = field.nextElementSibling;
                    if (!nextElement || !nextElement.classList.contains('invalid-feedback')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('invalid-feedback');
                        errorMsg.textContent = 'Bidang ini wajib diisi';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    });
    
    // Reset form validation pada input
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
});

// Fungsi untuk menambahkan animasi ketik pada judul
function typeWriter(element, text, i = 0, speed = 50) {
    if (i < text.length) {
        element.innerHTML += text.charAt(i);
        i++;
        setTimeout(function() {
            typeWriter(element, text, i, speed);
        }, speed);
    }
}
from django.shortcuts import render

def about(request):
    return render(request, 'pages/about.html', {
        'title': 'About Us',
        'description': 'Learn more about our student portal and mission.'
    })

def contact(request):
    return render(request, 'pages/contact.html', {
        'title': 'Contact Us',
        'description': 'Get in touch with our support team.'
    })

def faq(request):
    return render(request, 'pages/faq.html', {
        'title': 'Frequently Asked Questions',
        'description': 'Find answers to common questions about our student portal.'
    })

def privacy(request):
    return render(request, 'pages/privacy.html', {
        'title': 'Privacy Policy',
        'description': 'Learn about how we protect your data and privacy.'
    }) 
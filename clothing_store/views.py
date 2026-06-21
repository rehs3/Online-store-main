from django.shortcuts import render


def help_center(request):
	faqs = [
		{"q": "Como rastrear meu pedido?", "a": "Você pode rastrear seu pedido pelo link de rastreamento enviado por e-mail."},
		{"q": "Qual é o prazo de troca/devolução?", "a": "O prazo é de 30 dias a partir do recebimento do produto."},
		{"q": "Quais as formas de pagamento aceitas?", "a": "Aceitamos cartões, boleto e PayPal."},
		{"q": "Como alterar meu endereço?", "a": "Vá em seu perfil > Endereços e edite o endereço desejado."},
		{"q": "Esqueci minha senha. o que fazer?", "a": "Use a opção 'Esqueci minha senha' na tela de login para redefinir."},
	]
	contact = {
		"email": "Suporte@HSBC.com",
		"hours": [
			"Segunda a Sexta: das 08h ás 18h.",
			"Sábado: das 10h ás 14h",
			"Feriados: Fechado",
		],
	}
	return render(request, "help_center.html", {"faqs": faqs, "contact": contact})


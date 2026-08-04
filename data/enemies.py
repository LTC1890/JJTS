
import random 

BOSS_ABILITIES ={
"Mahito":[
{"name":"Toque da Alma","dmg_mult":1.88 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.8 ,
"desc":"Toca a alma - ignora defesa fisica"},
{"name":"Distorcao Corporal","dmg_mult":2.25 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"desc":"Deforma o corpo do alvo"},
{"name":"Transfiguracao Polimorfa","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Transforma o alvo em aberracao"},
{"name":"Body Repel","dmg_mult":2.5 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"desc":"Empurra com forca espiritual"},
],
"Jogo":[
{"name":"Ember Insects","dmg_mult":1.75 ,"effect":"burn","effect_value":4 ,"effect_chance":0.8 ,
"desc":"Insetos de fogo que queimam"},
{"name":"Maximum: Meteor","dmg_mult":3.75 ,"effect":"burn","effect_value":6 ,"effect_chance":0.6 ,
"desc":"Meteoro de fogo amaldicoado"},
{"name":"Coffin of the Iron Mountain","dmg_mult":3.12 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"desc":"Dominio parcial - montanha de ferro"},
{"name":"Piercing Blood","dmg_mult":2.75 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Lanca de sangue perfurante"},
],
"Sukuna":[
{"name":"Dismantle","dmg_mult":2.6 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.95 ,
"desc":"Corte conceitual - despedaca"},
{"name":"Cleave","dmg_mult":3.2 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.9 ,
"desc":"Corte automatico - se ajusta a resistencia"},
{"name":"Kamutoke: Trovao Divino","dmg_mult":4.5 ,"effect":"stun","effect_value":2 ,"effect_chance":0.55 ,
"desc":"Convoca sua ferramenta amaldicoada em forma de vajra e desce um raio absurdo do ceu"},
{"name":"Hiten: Chama Divina","dmg_mult":5.0 ,"effect":"burn","effect_value":9 ,"effect_chance":0.85 ,
"desc":"Golpeia com seu tridente amaldicoado, liberando uma chama capaz de incinerar tudo"},
{"name":"World Cutting Slash","dmg_mult":6.5 ,"effect":"bleed","effect_value":10 ,"effect_chance":1.0 ,
"desc":"Corte que divide o mundo"},
{"name":"Spiderweb Cut","dmg_mult":3.0 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.85 ,
"desc":"Cortes em teia"},
],
"Hanami":[
{"name":"Wooden Ball","dmg_mult":2.25 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"desc":"Esfera de madeira amaldicoada"},
{"name":"Flower Field","dmg_mult":2.5 ,"effect":"poison","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Campo de flores venenosas"},
{"name":"Cursed Vines","dmg_mult":3.12 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"desc":"Vinhas amaldicoadas prendem"},
{"name":"Hanami's Wrath","dmg_mult":3.75 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.6 ,
"desc":"Furia da natureza"},
],
"Mahoraga":[
{"name":"Espada da Roda","dmg_mult":3.0 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.8 ,
"desc":"Golpe com a roda divina"},
{"name":"Adaptacao Destrutiva","dmg_mult":3.5 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.75 ,
"desc":"Ataque adaptado +10% ATK"},
{"name":"Punho Adaptativo","dmg_mult":2.6 ,"effect":"stun","effect_value":2 ,"effect_chance":0.55 ,
"desc":"Soco adaptativo"},
{"name":"Roda Girante","dmg_mult":4.0 ,"effect":"stun","effect_value":1 ,"effect_chance":0.5 ,
"desc":"Roda gira em velocidade maxima"},
{"name":"Chama Adaptativa","dmg_mult":3.2 ,"effect":"burn","effect_value":5 ,"effect_chance":0.6 ,
"desc":"Mahoraga absorve e devolve fogo amaldicoado"},
],
"Toji Fushiguro":[
{"name":"Ataque Rapido","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Velocidade sobre-humana"},
{"name":"Ataque Furtivo","dmg_mult":3.75 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.6 ,
"desc":"Aparece do nada"},
{"name":"Garra Amaldicoada","dmg_mult":3.12 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"desc":"Garra que atordoa"},
{"name":"Inversor de Espiritos: Corte","dmg_mult":4.38 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.8 ,
"desc":"Arma amaldicoada lendaria - corta tecnicas amaldicoadas"},
{"name":"Inversor de Espiritos: Anulacao","dmg_mult":3.5 ,"effect":"technique_seal","effect_value":2 ,"effect_chance":0.5 ,
"desc":"A lamina anula tecnicas amaldicoadas - sela sua proxima tecnica"},
{"name":"Ponto Cego do Feiticeiro","dmg_mult":5.5 ,"effect":"bleed","effect_value":8 ,"effect_chance":0.95 ,
"def_ignore_pct":0.6 ,
"desc":"Ataca o ponto cego que so feiticeiros tem - dano massivo ignorando 60% da DEF"},
],
"Geto Suguru":[
{"name":"Maximum: Uzumaki","dmg_mult":3.75 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Vortice de maldicoes"},
{"name":"Rainbow Dragon","dmg_mult":3.12 ,"effect":"burn","effect_value":4 ,"effect_chance":0.6 ,
"desc":"Dragao arco-iris"},
{"name":"Invocacao em Massa","dmg_mult":2.5 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"desc":"Multiplas maldicoes atacando"},
{"name":"Manipulacao de Maldicoes","dmg_mult":3.5 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Controla maldicoes capturadas"},
],
"Choso":[
{"name":"Piercing Blood","dmg_mult":3.0 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.9 ,
"desc":"Jato de sangue perfurante"},
{"name":"Supernova","dmg_mult":4.0 ,"effect":"burn","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Explosao de sangue"},
{"name":"Convergence","dmg_mult":3.5 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.8 ,
"desc":"Comprime sangue e dispara"},
{"name":"Blood Manipulation","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Manipula sangue do alvo"},
],
"Satoru Gojo (Boss)":[
{"name":"Infinity","dmg_mult":0.0 ,"effect":None ,"effect_value":0 ,"effect_chance":0.0 ,
"desc":"Infinity bloqueia todo dano"},
{"name":"Blue","dmg_mult":2.5 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"desc":"Atrai e esmaga"},
{"name":"Red","dmg_mult":4.0 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Repulsa brutal"},
{"name":"Hollow Purple","dmg_mult":13.0 ,"effect":"bleed","effect_value":8 ,"effect_chance":0.9 ,
"desc":"Aniquilacao conceitual"},
{"name":"Unlimited Void","dmg_mult":5.0 ,"effect":"stun","effect_value":5 ,"effect_chance":1.0 ,
"desc":"Dominio - sobrecarga total"},
],
"Satoru Gojo (Boss) - Final Arc":[
{"name":"Domain Amplification: Seis Olhos Total","dmg_mult":4.0 ,"effect":"stun","effect_value":2 ,"effect_chance":0.65 ,
"desc":"Amplifica a propria Tecnica Amaldicoada Inerente ao limite - a mesma jogada usada contra Sukuna"},
{"name":"Maximum: Blue","dmg_mult":6.0 ,"effect":"stun","effect_value":3 ,"effect_chance":0.7 ,
"desc":"Versao amplificada de Blue - atracao capaz de esmagar qualquer coisa"},
{"name":"Maximum: Red","dmg_mult":8.5 ,"effect":"bleed","effect_value":9 ,"effect_chance":0.85 ,
"desc":"Versao amplificada de Red - repulsa capaz de destruir um quarteirao"},
{"name":"Hollow Purple: Aniquilacao Total","dmg_mult":18.0 ,"effect":"bleed","effect_value":12 ,"effect_chance":0.95 ,
"desc":"Hollow Purple a queima-roupa, amplificado pelo Domain Amplification - a cena que quase decidiu "
"a luta contra Sukuna"},
{"name":"Six Eyes: Leitura Perfeita","dmg_mult":3.5 ,"effect":"stun","effect_value":1 ,"effect_chance":0.75 ,
"desc":"Le cada movimento do oponente antes mesmo dele acontecer e contra-ataca"},
],
"Yuji Itadori (Boss)":[
{"name":"Divergent Fist","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Punho com atraso de CE"},
{"name":"Black Flash","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.4 ,
"desc":"Piscar negro"},
{"name":"Reforco Total","dmg_mult":2.25 ,"effect":"stun","effect_value":1 ,"effect_chance":0.3 ,
"desc":"Reforco corporal maximo"},
{"name":"Sukuna's Cleave","dmg_mult":4.38 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.6 ,
"desc":"Sukuna toma controle brevemente"},
],
"Megumi Fushiguro (Boss)":[
{"name":"Divine Dogs","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.8 ,
"desc":"Cachorros divinos"},
{"name":"Nue","dmg_mult":2.25 ,"effect":"stun","effect_value":1 ,"effect_chance":0.5 ,
"desc":"Ave eletrica"},
{"name":"Max Elephant","dmg_mult":3.12 ,"effect":"stun","effect_value":2 ,"effect_chance":0.4 ,
"desc":"Elefante colossal"},
{"name":"Mahoraga","dmg_mult":5.0 ,"effect":"bleed","effect_value":8 ,"effect_chance":0.7 ,
"desc":"Invoca Mahoraga em desespero"},
],
"Kento Nanami (Boss)":[
{"name":"Ratio: Ponto Fraco","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Acha ponto 7:3"},
{"name":"Collapse","dmg_mult":3.75 ,"effect":"stun","effect_value":2 ,"effect_chance":0.5 ,
"desc":"Colapso estrutural"},
{"name":"7:3 Critical","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.6 ,
"desc":"Critico no ponto fraco"},
{"name":"Black Flash","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.4 ,
"desc":"Piscar negro"},
],
"Maki Zenin (Boss)":[
{"name":"Ataque Fisico","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Forca sobre-humana"},
{"name":"Arma Amaldicoada","dmg_mult":3.75 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.6 ,
"desc":"Arma amaldicoada"},
{"name":"Esquiva Perfeita","dmg_mult":1.88 ,"effect":"stun","effect_value":1 ,"effect_chance":0.4 ,
"desc":"Esquiva e contra-ataca"},
{"name":"Furia Zenin","dmg_mult":4.38 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.7 ,
"desc":"Furia do cla Zenin"},
],
"Aoi Todo (Boss)":[
{"name":"Troca de Posicao","dmg_mult":1.88 ,"effect":"stun","effect_value":1 ,"effect_chance":0.6 ,
"desc":"Boogie Woogie"},
{"name":"Combo de Troca","dmg_mult":3.12 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Troca + ataque"},
{"name":"Soco Brutal","dmg_mult":3.75 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.6 ,
"desc":"Soco devastador"},
{"name":"Black Flash","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.4 ,
"desc":"Piscar negro"},
],
"Nobara Kugisaki (Boss)":[
{"name":"Pregos de CE","dmg_mult":2.25 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.8 ,
"desc":"Pregos amaldicoados"},
{"name":"Martelo Kugisaki","dmg_mult":3.12 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Martelo + prego"},
{"name":"Resonance","dmg_mult":4.38 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.6 ,
"desc":"Ressonancia - dano a distancia"},
{"name":"Hairbag","dmg_mult":2.5 ,"effect":"stun","effect_value":1 ,"effect_chance":0.5 ,
"desc":"Saco de cabelos"},
],
"Naoya Zenin":[
{"name":"Movimento 24fps","dmg_mult":3.12 ,"effect":"stun","effect_value":1 ,"effect_chance":0.6 ,
"desc":"Velocidade sobre-humana"},
{"name":"Congelamento de Quadro","dmg_mult":1.88 ,"effect":"stun","effect_value":2 ,"effect_chance":0.7 ,
"desc":"Congela o alvo"},
{"name":"Esquiva Perfeita","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.5 ,
"desc":"Esquiva + contra-ataque"},
{"name":"Max Speed","dmg_mult":3.75 ,"effect":"stun","effect_value":2 ,"effect_chance":0.6 ,
"desc":"Velocidade maxima"},
],
"Haruta Shigemo":[
{"name":"Ataque Sorrateiro","dmg_mult":2.5 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.7 ,
"desc":"Ataque pelas costas"},
{"name":"Miracle Save","dmg_mult":0.62 ,"effect":"stun","effect_value":1 ,"effect_chance":0.3 ,
"desc":"Sorte amaldicoada - sobrevive e contra-ataca"},
{"name":"Garra Rapida","dmg_mult":2.25 ,"effect":"bleed","effect_value":3 ,"effect_chance":0.6 ,
"desc":"Garras rapidas"},
{"name":"Fuga Cobard","dmg_mult":1.25 ,"effect":None ,"effect_value":0 ,"effect_chance":0.0 ,
"desc":"Tenta fugir (mas fica pra lutar)"},
],
"Yuta Okkotsu":[
{"name":"Play Cool e Sukiyaki","dmg_mult":2.8 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.75 ,
"desc":"Corte duplo com as duas katanas amaldicoadas"},
{"name":"Copia Amaldicoada","dmg_mult":2.8 ,"effect":"stun","effect_value":1 ,"effect_chance":0.35 ,
"desc":"Copia e reflete a ultima tecnica que o atingiu"},
{"name":"Rika Desperta","dmg_mult":3.4 ,"effect":"bleed","effect_value":6 ,"effect_chance":0.85 ,
"desc":"Rika manifesta um braco espectral, mais forte quanto mais Yuta sofre"},
{"name":"Cursed Womb: Forma Completa","dmg_mult":4.5 ,"effect":"bleed","effect_value":9 ,"effect_chance":0.9 ,
"desc":"Rika se manifesta em sua forma verdadeira e devastadora"},
],
"Hakari Kinji":[
{"name":"Ittadakimasu","dmg_mult":2.4 ,"effect":"bleed","effect_value":4 ,"effect_chance":0.6 ,
"desc":"Absorve a energia vital do alvo como pagamento do contrato"},
{"name":"Idle Death Gamble: Carta Numerica","dmg_mult":2.3 ,"effect":None ,"effect_value":0 ,"effect_chance":0.0 ,
"desc":"A aposta segura da maquina caca-niqueis"},
{"name":"Idle Death Gamble: Joker","dmg_mult":3.4 ,"effect":"stun","effect_value":1 ,"effect_chance":0.45 ,
"desc":"A carta mais arriscada - tudo ou nada"},
{"name":"Star Rage","dmg_mult":5.5 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.8 ,
"desc":"O soco lendario, concentrando toda a sorte acumulada"},
],
"Kenjaku":[
{"name":"Bisturi Amaldicoado","dmg_mult":2.3 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.75 ,
"desc":"Corte cirurgico preciso, direto nos pontos vitais"},
{"name":"Fusao de Maldicoes","dmg_mult":3.2 ,"effect":"poison","effect_value":5 ,"effect_chance":0.6 ,
"desc":"Funde fragmentos de maldicoes em um ataque instavel"},
{"name":"Transfiguracao Idle","dmg_mult":2.7 ,"effect":"stun","effect_value":2 ,"effect_chance":0.4 ,
"desc":"Reescreve a estrutura celular do alvo"},
{"name":"Xadrez de Mil Anos","dmg_mult":3.6 ,"effect":"stun","effect_value":1 ,"effect_chance":0.5 ,
"desc":"Um golpe calculado passos a frente de qualquer reacao"},
],
"Sukuna (Corpo de Megumi)":[
{"name":"Dismantle","dmg_mult":2.8 ,"effect":"bleed","effect_value":7 ,"effect_chance":0.9 ,
"desc":"Corte invisivel que despedaca a carne"},
{"name":"Cleave","dmg_mult":3.4 ,"effect":"bleed","effect_value":8 ,"effect_chance":0.85 ,
"desc":"Corte amplo que se ajusta a qualquer esquiva"},
{"name":"Mahoraga: Adaptacao Instantanea","dmg_mult":4.5 ,"effect":"stun","effect_value":2 ,"effect_chance":0.55 ,
"desc":"Convoca o shikigami mais forte de Megumi e o forca a se adaptar em segundos, algo que nem "
"Megumi conseguia controlar"},
{"name":"Divine Dogs: Mordida Dupla","dmg_mult":2.9 ,"effect":"bleed","effect_value":5 ,"effect_chance":0.7 ,
"desc":"Invoca os Cachorros Divinos de Megumi para atacar em duas frentes"},
{"name":"World Cutting Slash","dmg_mult":6.0 ,"effect":"bleed","effect_value":10 ,"effect_chance":0.95 ,
"desc":"Um corte que divide o proprio espaco"},
],
"Heitor Careca":[
{"name":"Infinity: Muralha Absoluta","dmg_mult":0.0 ,"effect":None ,"effect_value":0 ,"effect_chance":0.0 ,
"desc":"Um infinito que nada consegue atravessar"},
{"name":"Blue Devastador","dmg_mult":3.5 ,"effect":"stun","effect_value":2 ,"effect_chance":0.6 ,
"desc":"Atrai e esmaga com forca esmagadora"},
{"name":"Dismantle Supremo","dmg_mult":3.8 ,"effect":"bleed","effect_value":8 ,"effect_chance":0.95 ,
"desc":"Corte conceitual que despedaca qualquer coisa"},
{"name":"Cleave Absoluto","dmg_mult":4.2 ,"effect":"bleed","effect_value":9 ,"effect_chance":0.9 ,
"desc":"Corte que se ajusta e ignora qualquer resistencia"},
{"name":"Hollow Purple: Vazio Carmesim","dmg_mult":14.0 ,"effect":"bleed","effect_value":10 ,"effect_chance":0.9 ,
"desc":"Fusao impossivel de Blue e Red - aniquilacao conceitual"},
{"name":"World Cutting Slash: Fim Absoluto","dmg_mult":8.0 ,"effect":"bleed","effect_value":12 ,"effect_chance":1.0 ,
"desc":"Um corte que divide a propria realidade"},
],
}

CURSE_TEMPLATES ={
"Grau 4":[
{"name":"Maldicao Visceral","hp":50 ,"atk":8 ,"def":3 ,"speed":5 ,"ce":20 ,"xp":30 ,"drops_mult":0.5 },
{"name":"Maldicao Sombra","hp":40 ,"atk":10 ,"def":2 ,"speed":8 ,"ce":15 ,"xp":35 ,"drops_mult":0.5 },
{"name":"Maldicao Fede","hp":60 ,"atk":6 ,"def":4 ,"speed":4 ,"ce":25 ,"xp":25 ,"drops_mult":0.5 },
{"name":"Esporo Maldito","hp":35 ,"atk":12 ,"def":1 ,"speed":6 ,"ce":10 ,"xp":40 ,"drops_mult":0.6 },
],
"Grau 3":[
{"name":"Maldicao Ossuda","hp":90 ,"atk":14 ,"def":6 ,"speed":7 ,"ce":40 ,"xp":70 ,"drops_mult":0.8 },
{"name":"Maldicao Sangrenta","hp":80 ,"atk":18 ,"def":4 ,"speed":9 ,"ce":50 ,"xp":85 ,"drops_mult":0.8 },
{"name":"Maldicao Venenosa","hp":100 ,"atk":12 ,"def":7 ,"speed":6 ,"ce":35 ,"xp":75 ,"drops_mult":0.9 },
{"name":"Mascara Mutante","hp":110 ,"atk":16 ,"def":5 ,"speed":8 ,"ce":60 ,"xp":90 ,"drops_mult":0.9 },
],
"Grau 2":[
{"name":"Maldicao de Lâmina","hp":180 ,"atk":25 ,"def":10 ,"speed":12 ,"ce":80 ,"xp":150 ,"drops_mult":1.0 },
{"name":"Maldicao de Fogo","hp":200 ,"atk":28 ,"def":8 ,"speed":10 ,"ce":100 ,"xp":170 ,"drops_mult":1.0 },
{"name":"Maldicao Cyclope","hp":250 ,"atk":22 ,"def":14 ,"speed":7 ,"ce":90 ,"xp":160 ,"drops_mult":1.0 },
{"name":"Maldicao de Voo","hp":160 ,"atk":30 ,"def":6 ,"speed":16 ,"ce":110 ,"xp":180 ,"drops_mult":1.1 },
],
"Grau 1":[
{"name":"Carniceiro Amaldicoado","hp":380 ,"atk":42 ,"def":18 ,"speed":14 ,"ce":150 ,"xp":320 ,"drops_mult":1.5 },
{"name":"Maldicao Real","hp":420 ,"atk":45 ,"def":20 ,"speed":12 ,"ce":200 ,"xp":350 ,"drops_mult":1.5 },
{"name":"Colecionador de Almas","hp":350 ,"atk":50 ,"def":16 ,"speed":18 ,"ce":250 ,"xp":380 ,"drops_mult":1.6 },
{"name":"Maldicao do Espelho","hp":320 ,"atk":55 ,"def":22 ,"speed":20 ,"ce":280 ,"xp":400 ,"drops_mult":1.6 },
],
"Grau Especial":[
{"name":"Maldicao Primordial","hp":800 ,"atk":80 ,"def":30 ,"speed":22 ,"ce":500 ,"xp":1000 ,"drops_mult":3.0 },
{"name":"Filho de Sukuna","hp":700 ,"atk":95 ,"def":28 ,"speed":25 ,"ce":600 ,"xp":1200 ,"drops_mult":3.0 },
{"name":"Maldicao Conceitual","hp":900 ,"atk":75 ,"def":35 ,"speed":18 ,"ce":700 ,"xp":1100 ,"drops_mult":3.0 },
],
}

BOSSES ={
"Mahito":{
"name":"Mahito",
"rank":"Grau Especial",
"hp":170000 ,"max_hp":170000 ,"atk":3300 ,"def":1400 ,"speed":260 ,"ce":32000 ,"max_ce":32000 ,"xp":210000 ,
"desc":"Maldicao nascida do odio humano. Manipula a alma pelo toque.",
"immune_physical":True ,
"technique":"Idle Transfiguration",
"extensions_known":["Toque da Alma","Distorcao Corporal","Transfiguracao Polimorfa"],
"domain":"Self-Embodiment of Perfection",
"domain_ce_cost":2500 ,
"domain_dmg_mult":3.0 ,
"domain_trigger_hp_pct":0.40 ,
"domain_max_uses":2 ,
"domain_effect":"stun",
"domain_effect_value":2 ,
"ai_type":"smart_soul",
"ascii":"MAHITO",
"drops":["Coracao de Maldicao Especial","Cristal de CE","Cristal de CE"],"rare_drops":[{"item":"Selo de Status","chance":0.15}],
"karma_reward":-3 ,
"intro":"Mahito sorri. 'Vamos brincar com almas, humano?'",
"dodge_chance":0.25 ,
"crit_chance":0.18 ,
"stun_resist":0.50 ,
"bleed_resist":0.30 ,
"phases":[
{"hp_pct_below":0.6 ,"buff":{"atk":1.25 ,"speed":1.15 },"msg":"Mahito fica serio. O jogo mudou."},
{"hp_pct_below":0.3 ,"buff":{"atk":1.35 },"msg":"!! Mahito expande dominio: Self-Embodiment of Perfection !!"},
],
},
"Jogo":{
"name":"Jogo",
"rank":"Grau Especial",
"hp":150000 ,"max_hp":150000 ,"atk":4300 ,"def":950 ,"speed":230 ,"ce":30000 ,"max_ce":30000 ,"xp":190000 ,
"desc":"Maldicao do fogo. Disfarca-se de humano. Calmo e calculista.",
"immune_fire":True ,
"technique":"Manipulacao de Fogo",
"extensions_known":["Ember Insects","Maximum: Meteor","Coffin of the Iron Mountain"],
"domain":"Coffin of the Iron Mountain",
"domain_ce_cost":2800 ,
"domain_dmg_mult":3.2 ,
"domain_trigger_hp_pct":0.40 ,
"domain_max_uses":2 ,
"domain_effect":"burn",
"domain_effect_value":6 ,
"ai_type":"aoe_destroyer",
"ascii":"JOGO",
"drops":["Coracao de Maldicao Especial","Cristal de CE","Sangue Amaldicoado"],"rare_drops":[{"item":"Selo de Cura MAX","chance":0.2}],
"karma_reward":-3 ,
"intro":"Jogo inclina a cabeca. 'Voce eh uma desgraca para o futuro das maldicoes.'",
"burn_resist":0.70 ,
"crit_chance":0.16 ,
"phases":[
{"hp_pct_below":0.4 ,"buff":{"atk":1.5 },"msg":"Jogo chama seu dominio: COFFIN OF THE IRON MOUNTAIN!"},
],
},
"Sukuna":{
"name":"Sukuna (Heian)",
"rank":"Grau Especial",
"hp":440000 ,"max_hp":440000 ,"atk":6000 ,"def":1700 ,"speed":380 ,"ce":50000 ,"max_ce":50000 ,"xp":500000 ,
"desc":"O Rei das Maldicoes em sua forma verdadeira da era Heian: quatro bracos, dois rostos, vinte "
"dedos amaldicoados. Nessa forma ele carrega suas duas ferramentas amaldicoadas originais - "
"Kamutoke, em forma de vajra, e Hiten, o tridente ligado a sua Chama Divina - alem de Cleave e "
"Dismantle automaticos em suas outras mãos. O feiticeiro mais forte que a historia ja produziu, "
"e o mais perigoso encontro que um feiticeiro comum pode ter.",
"immune_physical":False ,
"technique":"Cleave and Dismantle",
"extensions_known":["Dismantle","Cleave","Kamutoke: Trovao Divino","Hiten: Chama Divina",
"Spiderweb Cut","World Cutting Slash"],
"domain":"Malevolent Shrine",
"domain_ce_cost":9500 ,
"domain_dmg_mult":7.0 ,
"domain_trigger_hp_pct":0.85 ,
"domain_max_uses":5 ,
"domain_effect":"bleed",
"domain_effect_value":12 ,
"ai_type":"god_mode",
"ascii":"SUKUNA",
"drops":["Dedo de Sukuna","Dedo de Sukuna","Dedo de Sukuna"],
"rare_drops":[{"item":"Anel de Sukuna","chance":0.20 },{"item":"Kamutoke","chance":0.25 },
{"item":"Hiten","chance":0.25 },{"item":"Anel do Caos","chance":0.10 }],
"karma_reward":-5 ,
"intro":"Sukuna abre os olhos lentamente, quatro bracos se manifestando ao seu redor. Em duas das "
"maos, Kamutoke e Hiten pulsam com CE antiga. 'Hm. Insetos ousam entrar no meu dominio? "
"Vou te ensinar o que e mil anos de superioridade.'",
"instakill_if_lower_rank":True ,
"can_active_rct":True ,
"rct_ce_cost":1400 ,
"rct_use_chance":0.38 ,
"rct_active_heal_pct":0.14 ,
"rct_pct":0.02 ,
"dodge_chance":0.42 ,
"defense_chance":0.34 ,
"crit_chance":0.36 ,
"crit_mult":2.6 ,
"stun_resist":0.80 ,
"bleed_resist":0.45 ,
"burn_resist":0.45 ,
"poison_resist":0.65 ,
"black_flash_chance":0.25 ,
"phases":[
{"hp_pct_below":0.85 ,"buff":{"atk":1.15 },"msg":"Sukuna abre os olhos. 'Oh? Voce me cortou. Interessante.'"},
{"hp_pct_below":0.65 ,"buff":{"atk":1.20 ,"crit_chance":0.08 },
"msg":"Sukuna sorri largamente e ergue Kamutoke. 'Bom. Mostre-me mais.'"},
{"hp_pct_below":0.40 ,"buff":{"atk":1.30 ,"speed":1.25 ,"dodge_chance":0.10 },
"msg":"!! Sukuna abre seu dominio: MALEVOLENT SHRINE !! 'Acabou.'"},
{"hp_pct_below":0.15 ,"buff":{"atk":1.55 ,"def":1.35 ,"crit_chance":0.12 },
"msg":"!! O REI DAS MALDICOES NAO RECUA !! Sukuna usa Kamutoke, Hiten e seus 4 bracos ao mesmo tempo."},
],
},
"Sukuna (Corpo de Megumi)":{
"name":"Sukuna, Rei das Maldicoes (Corpo de Megumi Fushiguro)",
"rank":"Grau Especial",
"hp":360000 ,"max_hp":360000 ,"atk":5200 ,"def":1500 ,"speed":360 ,"ce":45000 ,"max_ce":45000 ,"xp":900000 ,
"desc":"Apos consumir o corpo de Yuji Itadori, Sukuna encontra um vaso ainda mais perfeito em Megumi "
"Fushiguro - e com ele, herda tambem a Tecnica das Dez Sombras. O resultado e o Sukuna mais "
"aterrorizante ja visto: alem de suas proprias tecnicas devastadoras, ele agora comanda os "
"shikigami de Megumi a vontade, inclusive Mahoraga, forcando adaptacoes instantaneas que nem o "
"proprio Megumi jamais conseguiu controlar - foi assim que ele quebrou o Domain Amplification "
"de Gojo em segundos.",
"immune_physical":False ,
"technique":"Cleave and Dismantle (Sukuna)",
"extensions_known":["Dismantle","Cleave","Mahoraga: Adaptacao Instantanea","Divine Dogs: Mordida Dupla",
"World Cutting Slash"],
"domain":"Malevolent Shrine",
"domain_ce_cost":10000 ,
"domain_dmg_mult":7.0 ,
"domain_trigger_hp_pct":0.88 ,
"domain_max_uses":4 ,
"domain_effect":"bleed",
"domain_effect_value":12 ,
"adaptive":True ,
"adapt_speed_mult":3 ,
"ai_type":"smart",
"ascii":"SUKUNA_MEGUMI",
"drops":["Dedo de Sukuna","Dedo de Sukuna"],
"rare_drops":[{"item":"Anel de Sukuna","chance":0.20 },{"item":"Olho Roubado de Mahoraga","chance":0.25 }],
"karma_reward":40 ,
"intro":"O corpo de Megumi se move com uma frieza que nao e dele. Quatro bracos se manifestam, e as "
"sombras ao redor comecam a se contorcer, obedientes. 'Vamos ver quantas dessas sombras eu "
"consigo dominar antes de voce cair.'",
"can_active_rct":True ,
"rct_ce_cost":1200 ,
"rct_use_chance":0.35 ,
"rct_active_heal_pct":0.15 ,
"rct_pct":0.02 ,
"dodge_chance":0.40 ,
"defense_chance":0.32 ,
"crit_chance":0.32 ,
"crit_mult":2.3 ,
"stun_resist":0.70 ,
"bleed_resist":0.40 ,
"burn_resist":0.35 ,
"poison_resist":0.55 ,
"black_flash_chance":0.22 ,
"phases":[
{"hp_pct_below":0.70 ,"buff":{"atk":1.15 },
"msg":"Sukuna sorri com o rosto de Megumi. 'Interessante. Essas sombras respondem bem.'"},
{"hp_pct_below":0.45 ,"buff":{"atk":1.25 ,"speed":1.15 },
"msg":"!! Sukuna invoca Mahoraga e forca uma adaptacao instantanea !!"},
{"hp_pct_below":0.20 ,"buff":{"atk":1.40 ,"def":1.25 ,"crit_chance":0.10 },
"msg":"!! DEZ SOMBRAS E MALEVOLENT SHRINE JUNTOS !! 'Chega de brincadeira.'"},
],
},
"Yuta Okkotsu":{
"name":"Yuta Okkotsu",
"rank":"Grau Especial",
"hp":180000 ,"max_hp":180000 ,"atk":3800 ,"def":1050 ,"speed":320 ,"ce":35000 ,"max_ce":35000 ,"xp":220000 ,
"desc":"O feiticeiro mais forte da nova geracao. Ligado por um voto de amor e vinganca ao espirito "
"amaldicoado Rika, o espirito amaldicoado mais forte que ja existiu. Capaz de copiar qualquer "
"tecnica que observa de perto.",
"immune_physical":False ,
"technique":"Rika (Yuta Okkotsu)",
"extensions_known":["Play Cool e Sukiyaki: Corte Duplo","Rika Desperta: Braco Espectral","Copia Amaldicoada","Voto de Rika: Reversao Amaldicoada"],
"domain":"Cursed Womb: Straw Doll Technique",
"domain_ce_cost":8000 ,
"domain_dmg_mult":5.5 ,
"domain_trigger_hp_pct":0.85 ,
"domain_max_uses":3 ,
"domain_effect":"bleed",
"domain_effect_value":8 ,
"ai_type":"smart",
"ascii":"YUTA",
"drops":["Cristal de CE","Cristal de CE"],
"rare_drops":[{"item":"Anel do Caos","chance":0.10 }],
"karma_reward":15 ,
"intro":"Yuta desembainha as duas katanas. 'Desculpe, mas eu nao posso perder aqui. "
"Rika, me empresta sua forca.'",
"can_active_rct":True ,
"rct_ce_cost":900 ,
"rct_use_chance":0.40 ,
"rct_active_heal_pct":0.15 ,
"rct_pct":0.02 ,
"dodge_chance":0.35 ,
"defense_chance":0.28 ,
"crit_chance":0.30 ,
"crit_mult":2.2 ,
"stun_resist":0.65 ,
"bleed_resist":0.30 ,
"burn_resist":0.30 ,
"poison_resist":0.40 ,
"black_flash_chance":0.20 ,
"phases":[
{"hp_pct_below":0.80 ,"buff":{"atk":1.15 },"msg":"Yuta cerra os dentes. 'Rika, preciso de mais poder.'"},
{"hp_pct_below":0.55 ,"buff":{"atk":1.20 ,"crit_chance":0.08 },
"msg":"Rika sussurra atras de Yuta, os olhos brilhando de raiva."},
{"hp_pct_below":0.30 ,"buff":{"atk":1.30 ,"speed":1.20 ,"dodge_chance":0.08 },
"msg":"!! Yuta e Rika se movem como um so !!"},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-40 ,
},
"Hakari Kinji":{
"name":"Hakari Kinji",
"rank":"Grau Especial",
"hp":140000 ,"max_hp":140000 ,"atk":3200 ,"def":900 ,"speed":280 ,"ce":26000 ,"max_ce":26000 ,"xp":170000 ,
"desc":"Feiticeiro de grau semi-especial que aposta tudo em cada golpe. Sua tecnica Ittadakimasu converte "
"risco em poder bruto, culminando no lendario soco Star Rage.",
"immune_physical":False ,
"technique":"Ittadakimasu (Hakari Kinji)",
"extensions_known":["Ittadakimasu","Idle Death Gamble: Joker","Idle Death Gamble: Carta Numerica","Reversal: Red Bull"],
"domain":"Private Pure Love Train",
"domain_ce_cost":7000 ,
"domain_dmg_mult":5.0 ,
"domain_trigger_hp_pct":0.85 ,
"domain_max_uses":3 ,
"domain_effect":"stun",
"domain_effect_value":2 ,
"ai_type":"combo_swapper",
"ascii":"HAKARI",
"drops":["Sangue Amaldicoado","Cristal de CE"],
"rare_drops":[{"item":"Anel do Caos","chance":0.08 }],
"karma_reward":10 ,
"intro":"Hakari estala o pescoco com um sorriso largo. 'Beleza, vamos apostar tudo nessa aqui.'",
"can_active_rct":False ,
"dodge_chance":0.32 ,
"defense_chance":0.25 ,
"crit_chance":0.28 ,
"crit_mult":2.4 ,
"stun_resist":0.55 ,
"bleed_resist":0.20 ,
"burn_resist":0.20 ,
"poison_resist":0.30 ,
"black_flash_chance":0.25 ,
"phases":[
{"hp_pct_below":0.75 ,"buff":{"atk":1.15 },"msg":"Hakari ri. 'Agora sim ficou interessante.'"},
{"hp_pct_below":0.45 ,"buff":{"atk":1.25 ,"speed":1.15 },
"msg":"Hakari aposta tudo: 'Ittadakimasu!'"},
{"hp_pct_below":0.20 ,"buff":{"atk":1.40 ,"crit_chance":0.15 },
"msg":"!! Hakari prepara o Star Rage !!"},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-40 ,
},
"Kenjaku":{
"name":"Kenjaku",
"rank":"Grau Especial",
"hp":130000 ,"max_hp":130000 ,"atk":2600 ,"def":950 ,"speed":260 ,"ce":30000 ,"max_ce":30000 ,"xp":160000 ,
"desc":"O mestre por tras de mil anos de planejamento. Habita o corpo de Noritoshi Kamo e manipula "
"maldicoes, feiticeiros e a propria historia da jujutsu como pecas de um jogo de xadrez.",
"immune_physical":False ,
"technique":"Idle Transfiguration",
"extensions_known":["Bisturi Amaldicoado","Fusao de Maldicoes","Transfiguracao Idle","Xadrez de Mil Anos"],
"domain":None ,
"ai_type":"smart",
"ascii":"KENJAKU",
"drops":["Osso de Maldicao","Cristal de CE"],
"rare_drops":[{"item":"Anel do Caos","chance":0.10 }],
"karma_reward":-10 ,
"intro":"Kenjaku sorri de um jeito que nao pertence ao rosto que usa. "
"'Voce e uma peca interessante nesse tabuleiro.'",
"can_active_rct":False ,
"dodge_chance":0.30 ,
"defense_chance":0.30 ,
"crit_chance":0.22 ,
"crit_mult":2.0 ,
"stun_resist":0.60 ,
"bleed_resist":0.35 ,
"burn_resist":0.35 ,
"poison_resist":0.55 ,
"black_flash_chance":0.12 ,
"phases":[
{"hp_pct_below":0.70 ,"buff":{"def":1.15 },"msg":"Kenjaku recua um passo, recalculando."},
{"hp_pct_below":0.40 ,"buff":{"atk":1.20 ,"def":1.20 },
"msg":"'Interessante. Vou precisar me esforcar um pouco mais.'"},
{"hp_pct_below":0.15 ,"buff":{"atk":1.30 ,"speed":1.20 ,"crit_chance":0.10 },
"msg":"!! Kenjaku para de brincar !!"},
],
},
"Heitor Careca":{
"name":"HEITOR CARECA, O SUPERHONRADO",
"rank":"Grau Especial",
"hp":480000 ,"max_hp":480000 ,"atk":6800 ,"def":1900 ,"speed":420 ,"ce":60000 ,"max_ce":60000 ,"xp":1000000 ,
"desc":"Uma lenda que nao deveria existir. Um homem careca que, por algum motivo que ninguem consegue "
"explicar, domina simultaneamente a tecnica de Gojo, a tecnica de Sukuna, e adapta-se a qualquer "
"golpe em uma velocidade impossivel. Dizem que nem os mais fortes conseguem entender como ele existe.",
"immune_physical":False ,
"technique":"Limitless + Cleave and Dismantle",
"extensions_known":["Blue Devastador","Dismantle Supremo","Cleave Absoluto","Hollow Purple: Vazio Carmesim",
"World Cutting Slash: Fim Absoluto"],
"domain":"Trono do Vazio Carmesim",
"domain_ce_cost":11000 ,
"domain_dmg_mult":8.0 ,
"domain_trigger_hp_pct":0.90 ,
"domain_max_uses":5 ,
"domain_effect":"bleed",
"domain_effect_value":14 ,
"adaptive":True ,
"adapt_speed_mult":10 ,
"ai_type":"god_mode",
"ascii":"HEITOR",
"drops":["Dedo de Sukuna","Anel do Caos","Anel do Caos"],
"rare_drops":[{"item":"Anel de Sukuna","chance":0.35 },{"item":"Espelho de Rika","chance":0.10 }],
"karma_reward":50 ,
"intro":"Heitor Careca cruza os bracos e sorri, calmo. 'Voce chegou ate aqui, meus parabens de "
"verdade. Mas isso... isso e outro nivel.' Um sexto olho se abre em sua testa careca enquanto "
"quatro bracos se manifestam atras dele.",
"instakill_if_lower_rank":True ,
"can_active_rct":True ,
"rct_ce_cost":1500 ,
"rct_use_chance":0.40 ,
"rct_active_heal_pct":0.15 ,
"rct_pct":0.02 ,
"dodge_chance":0.45 ,
"defense_chance":0.38 ,
"crit_chance":0.38 ,
"crit_mult":2.6 ,
"stun_resist":0.85 ,
"bleed_resist":0.50 ,
"burn_resist":0.50 ,
"poison_resist":0.70 ,
"black_flash_chance":0.28 ,
"exclusive_boss":True ,
"requires_level":1100 ,
"phases":[
{"hp_pct_below":0.85 ,"buff":{"atk":1.15 },
"msg":"Heitor Careca abre um dos olhos. 'Interessante. Continue.'"},
{"hp_pct_below":0.65 ,"buff":{"atk":1.20 ,"crit_chance":0.08 },
"msg":"'Ok, agora eu vou ficar serio de verdade.'"},
{"hp_pct_below":0.45 ,"buff":{"atk":1.30 ,"speed":1.25 ,"dodge_chance":0.10 },
"msg":"!! Heitor Careca abre seu dominio: TRONO DO VAZIO CARMESIM !!"},
{"hp_pct_below":0.25 ,"buff":{"atk":1.45 ,"def":1.30 ,"crit_chance":0.12 },
"msg":"!! A RODA DE MAHORAGA DE HEITOR GIRA DEZ VEZES MAIS RAPIDO !! 'Voce ja nao tem mais nada que me surpreenda.'"},
{"hp_pct_below":0.10 ,"buff":{"atk":1.60 ,"def":1.40 ,"speed":1.30 ,"crit_chance":0.15 },
"msg":"!! HEITOR CARECA NAO CONHECE DERROTA !! 'Vamos ver ate onde voce consegue ir, de verdade.'"},
],
},
"Toji Fushiguro":{
"name":"Toji Fushiguro",
"rank":"Grau Especial",
"hp":160000 ,"max_hp":160000 ,"atk":5400 ,"def":1100 ,"speed":520 ,"ce":0 ,"max_ce":0 ,"xp":200000 ,
"desc":"Cacador de recompensas. Restricao Celestial total: zero CE mas corpo divino. "
"Sem CE proprio, tecnicas amaldicoadas comuns mal o alcancam - e o Inversor de "
"Espiritos em suas maos anula a tecnica de quem ele corta.",
"heavenly_restriction":True ,
"no_ce_tracking":True ,
"ce_dmg_resist":0.35 ,
"technique":"Nenhuma (Fisico Puro)",
"extensions_known":["Ataque Rapido","Ataque Furtivo","Garra Amaldicoada",
"Inversor de Espiritos: Corte","Inversor de Espiritos: Anulacao","Ponto Cego do Feiticeiro"],
"weapon":"Inversor de Espritos",
"ai_type":"speed_assassin",
"ascii":"TOJI",
"drops":["Cristal de CE","Cristal de CE","Osso de Maldicao"],"rare_drops":[{"item":"Inverted Spear of Heaven","chance":0.25},{"item":"Playful Cloud","chance":0.35}],
"karma_reward":0 ,
"intro":"Toji aparece do nada. 'Voce estava sendo seguido. Restricao Celestial: corpo perfeito, "
"zero CE. Sua tecnica nao vai significar nada pra mim.'",
"dodge_chance":0.45 ,
"crit_chance":0.30 ,
"crit_mult":2.2 ,
"first_strike_guaranteed":True ,
"phases":[
{"hp_pct_below":0.7 ,"buff":{"speed":1.15 },"msg":"Toji ja decorou seu padrao de movimento. 'Voce eh previsivel.'"},
{"hp_pct_below":0.4 ,"buff":{"atk":1.25 ,"speed":1.2 },"msg":"Toji acelera ao maximo. Sem CE, sem limites - so musculo e instinto."},
{"hp_pct_below":0.15 ,"buff":{"atk":1.3 ,"crit_chance":0.15 },"msg":"!! Toji para de brincar. O cacador de feiticeiros mostra por que matou Gojo. !!"},
],
},
"Hanami":{
"name":"Hanami",
"rank":"Grau Especial",
"hp":155000 ,"max_hp":155000 ,"atk":2900 ,"def":1650 ,"speed":180 ,"ce":26000 ,"max_ce":26000 ,"xp":195000 ,
"desc":"Maldicao da natureza. Nascida do medo humano da madre terra.",
"immune_plant":True ,
"technique":"Manipulacao de Madeira",
"extensions_known":["Wooden Ball","Flower Field","Cursed Vines"],
"domain":None ,
"ai_type":"tactical_defensive",
"ascii":"HANAMI",
"drops":["Coracao de Maldicao Especial","Sangue Amaldicoado"],"rare_drops":[{"item":"Selo de Cura Avancado","chance":0.3}],
"karma_reward":-2 ,
"intro":"Hanami fala suavemente. 'Eu quero salvar o planeta de voces.'",
"defense_chance":0.35 ,
"poison_resist":0.50 ,
"can_active_rct":True ,
"rct_ce_cost":600 ,
"rct_use_chance":0.30 ,
"rct_active_heal_pct":0.10 ,
"phases":[
{"hp_pct_below":0.4 ,"buff":{"def":1.5 },"msg":"Hanami cria armadura de madeira."},
],
},
"Mahoraga":{
"name":"Mahoraga (Shikigami)",
"rank":"Grau Especial",
"hp":48000 ,"max_hp":48000 ,"atk":1600 ,"def":520 ,"speed":260 ,"ce":10000 ,"max_ce":10000 ,"xp":55000 ,
"desc":"O shikigami mais poderoso das Dez Sombras. Adapta-se a qualquer tipo de "
"ataque que receber repetidamente, ganhando resistencia especifica contra ele. "
"Force-o a enfrentar algo novo, ou sera esmagado pela propria estrategia.",
"adaptive":True ,
"technique":"Adaptacao Conceitual",
"extensions_known":["Adaptacao","Espada da Roda","Punho Adaptativo","Roda Girante"],
"domain":None ,
"ai_type":"adaptive_tank",
"ascii":"MAHORAGA",
"drops":["Cristal de CE","Cristal de CE","Cristal de CE","Osso de Maldicao"],
"rare_drops":[{"item":"Selo de Forca","chance":0.45}],
"karma_reward":-1 ,
"intro":"A roda de Mahoraga gira. 'PRIMEIRO ADAPTACAO.' Ele observa seus movimentos.",
"dodge_chance":0.22 ,
"defense_chance":0.30 ,
"crit_chance":0.18 ,
"crit_mult":1.9 ,
"stun_resist":0.40 ,
"phases":[
{"hp_pct_below":0.6 ,"buff":{"def":1.25 },"msg":"Mahoraga adapta-se a sua presenca em combate."},
{"hp_pct_below":0.3 ,"buff":{"atk":1.45 ,"def":1.30 ,"speed":1.20 },
"msg":"Mahoraga completa a adaptacao final: AGORA, ANIQUILACAO."},
],
},
"Geto Suguru":{
"name":"Geto Suguru",
"rank":"Grau Especial",
"hp":160000 ,"max_hp":160000 ,"atk":3000 ,"def":1000 ,"speed":220 ,"ce":42000 ,"max_ce":42000 ,"xp":205000 ,
"desc":"Feiticeiro renegado. Controla maldicoes que capturou. Ideologo do genocidio nao-feiticeiros.",
"technique":"Manipulacao de Maldicoes",
"extensions_known":["Maximum: Uzumaki","Rainbow Dragon","Invocacao em Massa"],
"domain":None ,
"ai_type":"summoner_swarm",
"ascii":"GETO",
"drops":["Coracao de Maldicao Especial","Selo de Aprisionamento"],"rare_drops":[{"item":"Espelho de Rika","chance":0.25},{"item":"Caixa Amaldicoada","chance":0.3}],
"karma_reward":-3 ,
"intro":"Geto sorri calmamente. 'Vamos criar um mundo so de feiticeiros.'",
"crit_chance":0.18 ,
"phases":[
{"hp_pct_below":0.5 ,"buff":{"atk":1.15 },"msg":"Geto sorri. 'Acho que vou apresentar voce a alguns amigos.' Ele invoca maldicoes capturadas!","summon_curses":True },
{"hp_pct_below":0.25 ,"buff":{"atk":1.25 ,"speed":1.15 },"msg":"Geto libera Maldicao Especial Uzumaki em desespero."},
],
},
"Choso":{
"name":"Choso",
"rank":"Grau Especial",
"hp":95000 ,"max_hp":95000 ,"atk":2500 ,"def":750 ,"speed":210 ,"ce":20000 ,"max_ce":20000 ,"xp":120000 ,
"desc":"Irmao de Yuji (por sangue). Mestre em Manipulacao de Sangue. Vinganca pela familia.",
"technique":"Manipulacao de Sangue",
"extensions_known":["Piercing Blood","Supernova","Convergence","Blood Manipulation"],
"domain":None ,
"ai_type":"ranged_kiter",
"ascii":"CHOSO",
"drops":["Sangue Amaldicoado","Sangue Amaldicoado","Cristal de CE"],"rare_drops":[{"item":"Sangue Amaldicoado","chance":0.5}],
"karma_reward":0 ,
"intro":"Choso te encara. 'Voce matou meus irmaos?'",
"bleed_resist":0.30 ,
"phases":[
{"hp_pct_below":0.5 ,"buff":{"atk":1.4 },"msg":"Choso fica furioso. SANGUE PROPULSAO MAXIMO."},
{"hp_pct_below":0.2 ,"buff":{"atk":1.2 ,"def":1.2 },"msg":"Choso entra em Flecha de Sangue: modo final."},
],
},
"Naoya Zenin":{
"name":"Naoya Zenin",
"rank":"Grau 1",
"hp":8500 ,"max_hp":8500 ,"atk":480 ,"def":170 ,"speed":260 ,"ce":2200 ,"max_ce":2200 ,"xp":12000 ,
"desc":"Heir do cla Zenin. Misogino e cruel. Usuario de Projection Sorcery.",
"technique":"Projection Sorcery",
"extensions_known":["Movimento 24fps","Congelamento de Quadro","Esquiva Perfeita"],
"domain":None ,
"ai_type":"speed_striker",
"ascii":"NAOYA",
"drops":["Cristal de CE","Osso de Maldicao"],"rare_drops":[{"item":"Selo de CE Avancado","chance":0.4}],
"karma_reward":-1 ,
"intro":"Naoya ri. 'Voce? Um inseto como voce pensa que pode me derrotar?'",
"dodge_chance":0.35 ,
"crit_chance":0.22 ,
"phases":[
{"hp_pct_below":0.4 ,"buff":{"speed":1.3 },"msg":"Naoya acelera ao maximo. 'Vou te mostrar velocidade de verdade.'"},
],
},
"Haruta Shigemo":{
"name":"Haruta Shigemo",
"rank":"Grau 2",
"hp":5200 ,"max_hp":5200 ,"atk":320 ,"def":110 ,"speed":150 ,"ce":1100 ,"max_ce":1100 ,"xp":5500 ,
"desc":"Mercenario cruel. Sobrevive por sorte amaldicoada.",
"technique":"Miracle (Milagre)",
"extensions_known":["Miracle Save","Ataque Sorrateiro"],
"domain":None ,
"ai_type":"lucky_coward",
"ascii":"HARUTA",
"drops":["Cristal de CE","Osso de Maldicao"],"rare_drops":[{"item":"Pingente de Sorte","chance":0.2}],
"karma_reward":-1 ,
"intro":"Haruta rindo. 'Eh, eu sou sortudo. Voce vai perder.'",
"dodge_chance":0.20 ,
"phases":[],
},

"Satoru Gojo (Boss)":{
"name":"Satoru Gojo",
"rank":"Grau Especial",
"hp":220000 ,"max_hp":220000 ,"atk":1700 ,"def":750 ,"speed":340 ,"ce":20000 ,"max_ce":20000 ,"xp":80000 ,
"desc":"O feiticeiro mais forte. Os Seis Olhos te observam. Voce nao tem para onde correr. Se voce "
"conseguir levar essa luta ate o limite, vai ver por que ele e chamado de 'o mais forte' - a "
"mesma versao dele que foi para cima de Sukuna sem hesitar no arco final.",
"technique":"Limitless + Six Eyes",
"extensions_known":["Infinity","Blue","Red","Hollow Purple","Unlimited Void"],
"domain":"Unlimited Void",
"domain_ce_cost":7000 ,
"domain_dmg_mult":5.0 ,
"domain_trigger_hp_pct":0.50 ,
"domain_max_uses":2 ,
"domain_effect":"stun",
"domain_effect_value":2 ,
"ai_type":"god_mode",
"ascii":"GOJO",
"drops":["Talisma de Gojo","Cristal de CE","Cristal de CE"],"rare_drops":[{"item":"Bandana do Gojo","chance":0.3},{"item":"Talisma de Gojo","chance":0.5}],
"karma_reward":-30 ,
"intro":"Gojo aparece na sua frente. 'Eu nao posso te deixar fazer isso.'",
"instakill_if_lower_rank":False ,
"dmg_taken_mult":0.0 ,
"dodge_chance":0.40 ,
"defense_chance":0.25 ,
"crit_chance":0.30 ,
"crit_mult":2.2 ,
"stun_resist":0.65 ,
"bleed_resist":0.20 ,
"burn_resist":0.20 ,
"poison_resist":0.30 ,
"phases":[
{"hp_pct_below":0.70 ,"buff":{"atk":1.15 },"msg":"Gojo fica mais atento. 'Ok, voce e forte.'"},
{"hp_pct_below":0.45 ,"buff":{"atk":1.20 ,"dodge_chance":0.08 },
"msg":"Gojo fica serio. 'Vou parar de brincar agora.'"},
{"hp_pct_below":0.25 ,
"buff":{"atk":1.35 ,"def":1.25 ,"speed":1.20 ,"dodge_chance":0.12 ,"crit_chance":0.10 },
"new_extensions_known":["Domain Amplification: Seis Olhos Total","Maximum: Blue","Maximum: Red",
"Hollow Purple: Aniquilacao Total","Six Eyes: Leitura Perfeita"],
"new_abilities_key":"Satoru Gojo (Boss) - Final Arc",
"new_domain_dmg_mult":8.0 ,
"hp_bonus_pct":0.20 ,
"new_name":"Satoru Gojo (Arco Final)",
"msg":"!! GOJO PARA DE SEGURAR A PROPRIA FORCA !! 'Chega de meio-termo. Domain Amplification.' "
"Voce sente os Seis Olhos enxergarem cada milimetro do seu proximo movimento."},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-50 ,
},
"Kento Nanami (Boss)":{
"name":"Kento Nanami",
"rank":"Grau 1",
"hp":13000 ,"max_hp":13000 ,"atk":780 ,"def":300 ,"speed":210 ,"ce":3600 ,"max_ce":3600 ,"xp":26000 ,
"desc":"Feiticeiro profissional. Razao proporcional: 7:3. Veio te deter.",
"technique":"Razao Proporcional (Ratio)",
"extensions_known":["Ratio: Ponto Fraco","Collapse","Black Flash"],
"domain":None ,
"ai_type":"precise_striker",
"ascii":None ,
"drops":["Split Soul Katana","Cristal de CE","Sangue Amaldicoado"],"rare_drops":[{"item":"Split Soul Katana","chance":0.5}],
"karma_reward":-10 ,
"intro":"Nanami ajeita o relogio. 'Fora do horario de trabalho... mas preciso lidar com voce.'",
"black_flash_chance":0.35 ,
"weakpoint_bonus":0.50 ,
"crit_chance":0.22 ,
"defense_chance":0.30 ,
"phases":[
{"hp_pct_below":0.35 ,"buff":{"atk":1.25 },"msg":"Nanami acha seu ponto 7:3. 'Hora de terminar isso.'"},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-50 ,
},
"Megumi Fushiguro (Boss)":{
"name":"Megumi Fushiguro",
"rank":"Grau 1",
"hp":11000 ,"max_hp":11000 ,"atk":640 ,"def":260 ,"speed":230 ,"ce":4500 ,"max_ce":4500 ,"xp":22000 ,
"desc":"Herdou Dez Sombras. Convoca shikigamis para te caar.",
"technique":"Dez Sombras",
"extensions_known":["Divine Dogs","Nue","Max Elephant","Mahoraga"],
"domain":"Chimera Shadow Garden",
"domain_ce_cost":2000 ,
"domain_dmg_mult":2.8 ,
"domain_trigger_hp_pct":0.30 ,
"domain_max_uses":1 ,
"ai_type":"summoner_tactician",
"ascii":None ,
"drops":["Cristal de CE","Cristal de CE","Osso de Maldicao"],"rare_drops":[{"item":"Cristal de CE","chance":0.6}],
"karma_reward":-8 ,
"intro":"Megumi te encara. 'Voce se tornou uma maldicao. Vou te exorcizar.'",
"defense_chance":0.30 ,
"phases":[
{"hp_pct_below":0.3 ,"buff":{"atk":1.2 },"msg":"Megumi esta desesperado. 'Eu nao tenho escolha... PRIMEIRO ADAPTACAO!' Ele invoca Mahoraga!","summon_mahoraga":True },
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-40 ,
},
"Yuji Itadori (Boss)":{
"name":"Yuji Itadori",
"rank":"Grau 1",
"hp":13000 ,"max_hp":13000 ,"atk":680 ,"def":270 ,"speed":260 ,"ce":2800 ,"max_ce":2800 ,"xp":24000 ,
"desc":"Hospedeiro de Sukuna. Veio te parar antes que voce se torne uma ameaca maior.",
"technique":"Reforco Corporal + Divergent Fist",
"extensions_known":["Divergent Fist","Black Flash","Reforco Total"],
"domain":None ,
"ai_type":"aggressive_tank",
"ascii":None ,
"drops":["Cristal de CE","Sangue Amaldicoado","Punho de Ferro"],"rare_drops":[{"item":"Essencia de Alma do Yuji","chance":0.25}],
"karma_reward":-5 ,
"intro":"Yuji te encara com determinacao. 'Vou te parar antes que mais gente se machuque!'",
"black_flash_chance":0.35 ,
"dodge_chance":0.28 ,
"phases":[
{"hp_pct_below":0.4 ,"buff":{"atk":1.5 },"msg":"Yuji fica furioso. Sukuna ri dentro dele..."},
{"hp_pct_below":0.15 ,"buff":{"atk":1.3 ,"speed":1.2 },"msg":"Yuji deixa Sukuna assumir parcialmente o controle!"},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-30 ,
},
"Nobara Kugisaki (Boss)":{
"name":"Nobara Kugisaki",
"rank":"Grau 2",
"hp":8000 ,"max_hp":8000 ,"atk":480 ,"def":190 ,"speed":220 ,"ce":2300 ,"max_ce":2300 ,"xp":13500 ,
"desc":"Feiticeira do interior. Marretada e direta. Nao vai te deixar escapar.",
"technique":"Straw Doll Technique",
"extensions_known":["Prego Amaldicoado","Martelada Kugisaki","Hairpin","Ressonancia"],
"domain":None ,
"ai_type":"ranged_aggro",
"ascii":None ,
"drops":["Slaughter Demon","Punho de Ferro","Cristal de CE"],"rare_drops":[{"item":"Slaughter Demon","chance":0.4}],
"karma_reward":-5 ,
"intro":"Nobara aponta o martelo. 'Patetico. Vou te dar um presente no cranio.'",
"crit_chance":0.20 ,
"phases":[
{"hp_pct_below":0.35 ,"buff":{"atk":1.3 },"msg":"Nobara fica brava de verdade. 'Voce vai se arrepender.'"},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-25 ,
},
"Maki Zenin (Boss)":{
"name":"Maki Zenin",
"rank":"Grau 1",
"hp":11000 ,"max_hp":11000 ,"atk":820 ,"def":300 ,"speed":300 ,"ce":0 ,"max_ce":0 ,"xp":21000 ,
"desc":"Restricao Celestial total. Forca sobre-humana. Arma amaldicoada em maos.",
"technique":"Nenhuma (Fisico Puro)",
"extensions_known":["Ataque Fisico","Arma Amaldicoada","Esquiva Perfeita"],
"domain":None ,
"ai_type":"physical_striker",
"ascii":None ,
"drops":["Katana Amaldicoada Comum","Cristal de CE","Osso de Maldicao"],"rare_drops":[{"item":"Katana Amaldicoada Comum","chance":0.5}],
"karma_reward":-5 ,
"intro":"Maki te encara friamente. 'Fraqueza nao e desculpa. Saia do meu caminho ou morra.'",
"heavenly_restriction":True ,
"black_flash_chance":0.35 ,
"dodge_chance":0.35 ,
"crit_chance":0.25 ,
"phases":[
{"hp_pct_below":0.3 ,"buff":{"atk":1.3 ,"speed":1.2 },"msg":"Maki troca para a Katana Amaldicoada de Sao Lao."},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-35 ,
},
"Aoi Todo (Boss)":{
"name":"Aoi Todo",
"rank":"Grau 1",
"hp":12500 ,"max_hp":12500 ,"atk":760 ,"def":310 ,"speed":250 ,"ce":3200 ,"max_ce":3200 ,"xp":22000 ,
"desc":"Boogie Woogie. Troca posicoes e te da socos brutais.",
"technique":"Boogie Woogie",
"extensions_known":["Troca de Posicao","Combo de Troca","Soco Brutal"],
"domain":None ,
"ai_type":"combo_swapper",
"ascii":None ,
"drops":["Cristal de CE","Osso de Maldicao","Cristal de CE"],"rare_drops":[{"item":"Punho de Ferro","chance":0.4}],
"karma_reward":-5 ,
"intro":"Todo surge bufando. 'Voce virou uma aberracao. Vou te destruir como ao resto.'",
"black_flash_chance":0.30 ,
"crit_chance":0.20 ,
"phases":[
{"hp_pct_below":0.35 ,"buff":{"atk":1.3 },"msg":"Todo fica serio. 'Voce e meu melhor amigo agora. Por isso vou com tudo.'"},
],
"is_sorcerer_boss":True ,
"min_karma_to_appear":-30 ,
},
}

def generate_curse (rank =None ,level_mult =1.0 ,danger_mult =1.0 ):

    if rank is None :
        rank =random .choice (list (CURSE_TEMPLATES .keys ()))

    template =random .choice (CURSE_TEMPLATES [rank ])
    variance =0.85 +random .random ()*0.3 
    total_mult =variance *level_mult *danger_mult 

    name =_generate_curse_name (rank )

    rank_idx =RANK_ORDER .index (rank )if rank in RANK_ORDER else 0 
    extensions =[]
    technique ="Nenhuma"
    can_defend =False 
    can_dodge =False 
    ai_type ="basic"

    if rank_idx >=2 :
        can_defend =True 
        can_dodge =True 
        ai_type ="smart"

        if random .random ()<0.5 :
            technique ,extensions =_roll_random_technique_for_curse (rank )
    elif rank_idx ==1 :
        can_dodge =True 
        ai_type ="basic_smart"
        if random .random ()<0.25 :
            technique ,extensions =_roll_random_technique_for_curse (rank )

    curse ={
    "name":name ,
    "rank":rank ,
    "hp":max (1 ,int (template ["hp"]*total_mult )),
    "max_hp":max (1 ,int (template ["hp"]*total_mult )),
    "atk":max (1 ,int (template ["atk"]*total_mult )),
    "def":max (0 ,int (template ["def"]*total_mult )),
    "speed":max (1 ,int (template ["speed"]*total_mult )),
    "ce":max (0 ,int (template ["ce"]*total_mult )),
    "max_ce":max (0 ,int (template ["ce"]*total_mult )),
    "xp":int (template ["xp"]*level_mult ),
    "drops_mult":template ["drops_mult"],
    "is_boss":False ,
    "technique":technique ,
    "extensions_known":extensions ,
    "domain":None ,
    "ai_type":ai_type ,
    "ascii":None ,
    "phases":[],
    "karma_reward":-1 ,
    "abilities":_roll_curse_abilities_for_generate_curse (rank ),

    "can_defend":can_defend ,
    "can_dodge":can_dodge ,
    "can_crit":True ,
    "can_use_skills":True ,
    "dodge_chance":min (0.4 ,0.05 +(rank_idx *0.05 )),
    "defense_chance":min (0.4 ,0.10 +(rank_idx *0.05 )),
    "crit_chance":min (0.3 ,0.05 +(rank_idx *0.04 )),
    "crit_mult":1.5 +rank_idx *0.1 ,
    "stun_resist":min (0.55 ,0.05 +(rank_idx *0.10 )),
    }
    return curse 

def _roll_curse_abilities_for_generate_curse (rank ):

    from generator import CURSE_ABILITIES ,_get_rank_idx 
    rank_idx =_get_rank_idx (rank )
    eligible =[a for a in CURSE_ABILITIES if a ["min_rank_idx"]<=rank_idx ]
    if not eligible :
        return [CURSE_ABILITIES [0 ]]
    n =min (len (eligible ),max (2 ,2 +rank_idx //2 ))

    return random .sample (eligible ,min (n ,len (eligible )))

_CURSE_PREFIXES =[
"Visceral","Sombria","Fetida","Ossuda","Sangrenta","Venenosa",
"Mutante","Primordial","Antiga","Conceitual","Espectral","Torcido",
"Caotico","Amaldicoad","Imortal","Letal","Vingativa","Noturna",
]
_CURSE_THEMES =[
"do Abismo","do Vazio","do Sangue","da Morte","do Medo",
"do Caos","do Hatred","da Agonia","do Fogo","do Gelo",
"do Vento","da Terra","do Trovao","das Sombras","do Espelho",
"do Tempo","da Loucura","da Ruina","do Silencio","da Tormenta",
]

def _generate_curse_name (rank ):

    prefix =random .choice (_CURSE_PREFIXES )
    theme =random .choice (_CURSE_THEMES )

    if rank =="Grau Especial"and random .random ()<0.5 :
        titles =[", o Devorador",", a Besta",", Rainha das Maldicoes",
        ", Senhor do Caos",", Aniquilador"]
        return f"Maldicao {prefix } {theme }{random .choice (titles )}"
    return f"Maldicao {prefix } {theme }"

def _roll_random_technique_for_curse (rank ):

    curse_techniques =[
    ("Lamina de Sombra",["Corte Negro","Investida Sombria"]),
    ("Veneno CE",["Gas Toxico","Mordida Venenosa"]),
    ("Garra Amaldicoada",["Corte Vertical","Garra Rapida"]),
    ("Fogo Amaldicoado",["Bola de Fogo","Inferno"]),
    ("Gelo Amaldicoado",["Lanca de Gelo","Congelamento"]),
    ("Sangue Amaldicoado",["Piercing Blood","Supernova"]),
    ("Manipulacao de Osso",["Lanca Ossea","Armadura Ossea"]),
    ("Ilusao CE",["Espelho Quebrado","Mirages"]),
    ]
    tech_name ,ext_names =random .choice (curse_techniques )
    return tech_name ,ext_names 

def get_boss (boss_name ):

    boss_data =BOSSES .get (boss_name )
    if not boss_data :
        return None 
    import copy 
    boss =copy .deepcopy (boss_data )
    boss ["is_boss"]=True 
    boss ["max_hp"]=boss .get ("max_hp",boss .get ("hp"))
    boss ["max_ce"]=boss .get ("max_ce",boss .get ("ce",0 ))
    if boss_name in BOSS_ABILITIES :
        boss ["abilities"]=BOSS_ABILITIES [boss_name ]
    else :

        boss ["abilities"]=[]
    rank_idx ={"Grau 4":0 ,"Grau 3":1 ,"Grau 2":2 ,"Grau 1":3 ,"Grau Especial":4 }
    r_idx =rank_idx .get (boss .get ("rank","Grau 1"),3 )
    boss ["can_dodge"]=True 
    boss ["can_defend"]=True 
    boss ["can_crit"]=True 
    boss ["can_use_skills"]=True 
    boss .setdefault ("dodge_chance",min (0.50 ,0.10 +r_idx *0.05 ))
    boss .setdefault ("defense_chance",min (0.50 ,0.15 +r_idx *0.05 ))
    boss .setdefault ("crit_chance",min (0.40 ,0.10 +r_idx *0.05 ))
    boss .setdefault ("crit_mult",1.8 +r_idx *0.1 )
    boss .setdefault ("stun_resist",min (0.70 ,0.30 +r_idx *0.10 ))
    boss .setdefault ("bleed_resist",0.0 )
    boss .setdefault ("burn_resist",0.0 )
    boss .setdefault ("poison_resist",0.0 )
    return boss 

def random_boss (rank ="Grau Especial"):

    candidates =[name for name ,data in BOSSES .items ()
    if data .get ("rank")==rank and not data .get ("is_sorcerer_boss")and not data .get ("exclusive_boss")]
    if not candidates :
        candidates =[name for name ,data in BOSSES .items ()if not data .get ("exclusive_boss")]
    return get_boss (random .choice (candidates ))

def get_sorcerer_boss_by_karma (player_karma ,player_level ):

    available_sorcerers =[]
    for name ,data in BOSSES .items ():
        if not data .get ("is_sorcerer_boss"):
            continue 

        min_karma =data .get ("min_karma_to_appear",-100 )
        if player_karma <=min_karma :

            min_level_for_boss ={"Grau 2":5 ,"Grau 1":10 ,"Grau Especial":20 }
            min_lv =min_level_for_boss .get (data .get ("rank","Grau 1"),10 )
            if player_level >=min_lv :
                available_sorcerers .append (name )

    if not available_sorcerers :
        return None 
    return get_boss (random .choice (available_sorcerers ))

def list_sorcerer_bosses_by_karma (player_karma ,player_level ):

    available =[]
    for name ,data in BOSSES .items ():
        if not data .get ("is_sorcerer_boss"):
            continue 
        min_karma =data .get ("min_karma_to_appear",-100 )
        if player_karma <=min_karma :
            min_level_for_boss ={"Grau 2":5 ,"Grau 1":10 ,"Grau Especial":20 }
            min_lv =min_level_for_boss .get (data .get ("rank","Grau 1"),10 )
            if player_level >=min_lv :
                available .append (name )
    return available 

CURSE_PREFIXES =["Visceral","Sombria","Fetida","Ossuda","Sangrenta",
"Venenosa","Mutante","Primordial","Antiga","Conceitual"]
CURSE_SUFFIXES =["do Abismo","do Vazio","do Sangue","da Morte",
"do Medo","do Caos","do Hatred","do Desejo","da Agonia"]

def generate_random_curse_name ():
    return f"Maldicao {random .choice (CURSE_PREFIXES )} {random .choice (CURSE_SUFFIXES )}"

RANK_INFO ={
"Grau 4":{"xp_to_next_rank":500 ,"desc":"Maldicoes fracas. Apenas capazes de assombrar."},
"Grau 3":{"xp_to_next_rank":1500 ,"desc":"Maldicoes que podem ferir civis."},
"Grau 2":{"xp_to_next_rank":4000 ,"desc":"Maldicoes perigosas. Semi-1 e Semi-2."},
"Grau 1":{"xp_to_next_rank":10000 ,"desc":"Maldicoes mortais. Exigem equipe de feiticeiros."},
"Grau Especial":{"xp_to_next_rank":999999 ,"desc":"Maldicoes apocalipticas. Apenas elites podem enfrentar."},
}

RANK_ORDER =["Grau 4","Grau 3","Grau 2","Grau 1","Grau Especial"]

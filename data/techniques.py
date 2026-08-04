
import random 
import sys 
import os 

sys .path .insert (0 ,os .path .dirname (os .path .abspath (__file__ )))

from ui import Color ,c 

INNATE_TECHNIQUES ={
"Sem Tecnica":{
"weight":45 ,
"desc":"Voce nao possui uma tecnica inata. Mas isso nao te faz fraco - "
"seu corpo se torna um instrumento de CE pura.",
"rank_req":None ,
"color":"BRIGHT_WHITE",
"passive_bonus":{"ce_reinforcement":1.3 ,"physical_bonus":1.15 },
"extensions":[
{"name":"Reforco Corporal","desc":"Aumenta forca fisica e defesa por 3 turnos.","ce_cost":15 ,"type":"buff"},
{"name":"Lamina de CE","desc":"Cria uma lamina de energia amaldicoada na mao.","ce_cost":10 ,"type":"attack","dmg_mult":1.5 },
{"name":"Pulso de CE","desc":"Explosao curta de energia em area proxima.","ce_cost":18 ,"type":"attack_aoe","dmg_mult":1.2 },
{"name":"Golpe Carregado","desc":"Concentra CE no punho por um ataque devastador.","ce_cost":25 ,"type":"attack","dmg_mult":2.2 },
],
"domain":None ,
},

"Limitless":{
"weight":1 ,
"desc":("A tecnica do cla Gojo. Manipula e distorce o espaco em nivel conceitual. "
"EVOLUI: Comeca como Limitless (J) - Juventude. Apos atingir nivel 15 na tecnica, "
"desperta para a forma completa com skills muito mais poderosas."),
"rank_req":None ,
"color":"BRIGHT_CYAN",
"passive_bonus":{"dodge":1.5 ,"ce_efficiency":1.8 ,"control_bonus":1.4 },
"extensions":[

{"name":"Blue (J)","desc":"Atrai o alvo a um ponto, esmagando-o. 1.8x dano, sangramento 3t, 40% stun 5t.",
"ce_cost":35 ,"type":"attack","dmg_mult":1.8 ,"bleed":True ,"bleed_turns":3 ,
"stun_chance":0.40 ,"stun_turns":5 ,"requires_stage":"J"},
{"name":"Blue: Attraction Field (J)","desc":"Campo de atracao - +45% defesa por 4 turnos. Custo 12 CE/turno.",
"ce_cost":12 ,"type":"buff_def","duration":4 ,"buff_value":45 ,"requires_stage":"J"},
{"name":"Maximum Output: Blue (J)","desc":"Explosao massiva em todos os inimigos. 5x dano AOE, stun 3t.",
"ce_cost":75 ,"type":"attack_aoe","dmg_mult":5.0 ,"stun_turns":3 ,"requires_stage":"J"},

{"name":"Blue","desc":"Atrai o alvo com forca total. 2.5x dano, stun 3t, sangramento.",
"ce_cost":19 ,"type":"attack","dmg_mult":2.5 ,"bleed":True ,"stun_turns":3 ,
"requires_stage":"Despertado"},
{"name":"299 Seconds Run","desc":"Dano variado 25-95. Hit Kill se alvo for Grau 3 ou 4.",
"ce_cost":60 ,"type":"attack","dmg_mult":1.0 ,"variable_dmg":(25 ,95 ),
"instakill_below_rank":["Grau 3","Grau 4"],"requires_stage":"Despertado"},
{"name":"Red","desc":"Repulsa em area. 4x dano AOE, stun 3t, sangramento.",
"ce_cost":19 ,"type":"attack_aoe","dmg_mult":4.0 ,"bleed":True ,"stun_turns":3 ,
"requires_stage":"Despertado"},
{"name":"Maximum Output: Blue","desc":"Versao completa. 5x AOE, stun 3t.",
"ce_cost":25 ,"type":"attack_aoe","dmg_mult":5.0 ,"stun_turns":3 ,"requires_stage":"Despertado"},
{"name":"Maximum Output: Red","desc":"Repulsao massiva. 8x AOE.",
"ce_cost":25 ,"type":"attack_aoe","dmg_mult":8.0 ,"requires_stage":"Despertado"},
{"name":"Hollow Purple","desc":"Fusao Blue+Red. 13x dano, ignora 85% def.",
"ce_cost":55 ,"type":"attack","dmg_mult":13.0 ,"armor_pierce_pct":0.85 ,"requires_stage":"Despertado"},
{"name":"200% Hollow Purple","desc":"Versao potente. 21x dano. Requer HP < 40% ou carga 2 turnos.",
"ce_cost":75 ,"type":"attack","dmg_mult":21.0 ,"requires_stage":"Despertado",
"requires_hp_below_pct":0.40 },
{"name":"Hollow Purple: NUKE","desc":"DESTRUICAO TOTAL. 36x dano. Requer HP < 35% e CE 100%. 1 uso/luta.",
"ce_cost":200 ,"type":"attack","dmg_mult":36.0 ,"requires_stage":"Despertado",
"requires_hp_below_pct":0.35 ,"requires_ce_full":True ,"one_use_per_battle":True },
{"name":"Unlimited Void","desc":"EXPANSAO DE DOMINIO ATIVA. O vacuo infinito. Stun enquanto ativo, "
"ataque garantido, reducao de resistencia. Apos acabar: alvo fica parado 5 turnos e toma 50% da vida de dano. "
"Custo: 80 CE + 70 CE/turno. Dura ate CE acabar.",
"ce_cost":80 ,"type":"domain_active","domain_id":"unlimited_void",
"ce_per_turn":70 ,"dmg_per_turn_min":80 ,"dmg_per_turn_max":200 ,
"stun_all_per_turn":True ,"post_duration_stun":5 ,"post_duration_dmg_pct":0.50 ,
"requires_stage":"Despertado"},
],
"domain":"Unlimited Void",
},

"Dez Sombras":{
"weight":5 ,
"desc":("Tecnica ancestral do cla Zenin, herdada por Megumi Fushiguro apesar de nao ter sangue Zenin "
"puro. Usa sombras como portal para invocar ate dez shikigamis simultaneos - cada um consome uma 'sombra' "
"do total disponivel. O ápice da tecnica e domar Mahoraga, o shikigami mais poderoso, capaz de se "
"adaptar a qualquer ataque que sofre."),
"rank_req":None ,
"color":"BRIGHT_BLACK",
"passive_bonus":{"summon_power":1.0 ,"ce_regen":1.2 },
"extensions":[
{"name":"Invocar Divine Dogs","desc":"Cachorros Divinos - 2 lobos. Custo: 35 CE. Sustenta 12 CE/turno.","ce_cost":35 ,"type":"summon_shikigami","shikigami_id":"Divine Dogs"},
{"name":"Invocar Nue","desc":"Ave Eletrica. Custo: 40 CE. Sustenta 15 CE/turno.","ce_cost":40 ,"type":"summon_shikigami","shikigami_id":"Nue"},
{"name":"Invocar Great Serpent","desc":"Serpente colosal. Custo: 50 CE. Sustenta 18 CE/turno.","ce_cost":50 ,"type":"summon_shikigami","shikigami_id":"Great Serpent"},
{"name":"Invocar Toad","desc":"Sapo - atordoa 2 turnos. Custo: 25 CE.","ce_cost":25 ,"type":"summon_shikigami","shikigami_id":"Toad"},
{"name":"Invocar Max Elephant","desc":"Elefante. Custo: 70 CE. Sustenta 25 CE/turno.","ce_cost":70 ,"type":"summon_shikigami","shikigami_id":"Max Elephant"},
{"name":"Invocar Rabbit Escape","desc":"Coelhos - fuga em 2 turnos. Custo: 30 CE.","ce_cost":30 ,"type":"summon_shikigami","shikigami_id":"Rabbit Escape"},
{"name":"Invocar Round Deer","desc":"Cervo - cura 100 HP. Custo: 80 CE.","ce_cost":80 ,"type":"summon_shikigami","shikigami_id":"Round Deer"},
{"name":"Invocar Piercing Ox","desc":"Touro - 3 turnos. Custo: 65 CE.","ce_cost":65 ,"type":"summon_shikigami","shikigami_id":"Piercing Ox"},
{"name":"Invocar Mahoraga","desc":"Shikigami mais poderoso. Custo: 150 CE. Sustenta 50 CE/turno.","ce_cost":150 ,"type":"summon_shikigami","shikigami_id":"Eight-Handled Sword Mahoraga"},
{"name":"Invocar Merged Beast","desc":"Fusao de shikigamis. Requer Mahoraga domado. Custo: 200 CE.","ce_cost":200 ,"type":"summon_shikigami","shikigami_id":"Merged Beast"},
{"name":"Sombra Oculta","desc":"Esquiva garantida por 1 turno. Custo: 18 CE.","ce_cost":18 ,"type":"buff_dodge"},
{"name":"Chimera Shadow Garden","desc":"Expansao de dominio ativa. Certeiro em todos inimigos, "
"todos os shikigamis podem atacar livremente, dano 100-300/turno. "
"Custo: 80 CE + 40 CE/turno. Dura ate CE acabar.",
"ce_cost":80 ,"type":"domain_active","domain_id":"chimera_shadow_garden",
"ce_per_turn":40 ,"dmg_per_turn_min":100 ,"dmg_per_turn_max":300 ,
"bleed_per_turn":2 ,"summon_all":True },
],
"domain":"Chimera Shadow Garden",
},

"Manipulacao de Sangue":{
"weight":8 ,
"desc":("Tecnica do cla Kamo. Controla o proprio sangue dentro e fora do corpo. "
"v1.4.5: TODAS as skills custam 1 HP adicional (perde vida mesmo se errar). "
"Porem tem habilidades de cura (Crimson Healing) e o Blood Domain para compensar."),
"rank_req":None ,
"color":"RED",
"passive_bonus":{"hp_regen":1.1 ,"blood_efficiency":1.0 },
"extensions":[
{"name":"Piercing Blood","desc":"Jato de sangue perfurante. 2.4x dano, ignora 25% def, sangra 3t. Custo: 1 HP.",
"ce_cost":18 ,"type":"attack","dmg_mult":2.4 ,"armor_pierce_pct":0.25 ,"bleed":True ,"bleed_turns":3 ,
"hp_cost":1 },
{"name":"Supernova","desc":"Explosao de sangue em area. 3.2x AOE, dano extra em sangrando. Custo: 1 HP.",
"ce_cost":35 ,"type":"attack_aoe","dmg_mult":3.2 ,"bleed":True ,"bleed_turns":2 ,
"bonus_vs_bleeding":1.5 ,"hp_cost":1 },
{"name":"Flowing Red Scale","desc":"Buff: +35% forca, +30% velocidade, +15% esquiva por 4t. Custo: 1 HP.",
"ce_cost":20 ,"type":"buff","buff":"str","buff_mult":1.35 ,"speed_mult":1.30 ,
"dodge_bonus":0.15 ,"duration":4 ,"hp_cost":1 },
{"name":"Blood Edge","desc":"Lamina de sangue. 3.5x dano, ignora 40% def, sangra 4t. Custo: 1 HP.",
"ce_cost":28 ,"type":"attack","dmg_mult":3.5 ,"armor_pierce_pct":0.40 ,"bleed":True ,"bleed_turns":4 ,
"hp_cost":1 },
{"name":"Blood Bind","desc":"Prende com sangue. 1.8x dano, stun 2t, sangra 3t. Custo: 1 HP.",
"ce_cost":32 ,"type":"attack","dmg_mult":1.8 ,"bleed":True ,"bleed_turns":3 ,"stun_turns":2 ,
"hp_cost":1 },
{"name":"Crimson Healing","desc":"Cura 20% HP maximo + 3% por inimigo sangrando. Remove sangramento. Custo: 1 HP.",
"ce_cost":30 ,"type":"heal","heal_pct":0.20 ,"extra_heal_per_bleeding_enemy":0.03 ,
"remove_self_bleed":True ,"hp_cost":1 },
{"name":"Blood Domain","desc":"Expansao de dominio. Sangramento em todos inimigos/turno + cura por turno. "
"Custo: 65 CE + 30 CE/turno. Dura ate CE acabar.",
"ce_cost":65 ,"type":"domain_active","domain_id":"blood_domain",
"ce_per_turn":30 ,"hp_cost":0 ,
"dmg_per_turn_min":30 ,"dmg_per_turn_max":60 ,
"bleed_per_turn":3 ,"heal_per_turn_pct":0.05 },
],
"domain":"Blood Domain",
},

"Discurso Amaldicoado":{
"weight":4 ,
"desc":("Tecnica do cla Inumaki. Palavras ditas com CE se tornam ordens absolutas que o corpo do alvo "
"e obrigado a obedecer. O preco e alto: cada comando desgasta a propria garganta do usuario, que "
"por isso passa o dia a dia falando so em nomes de recheio de onigiri (salmao, salmao) para nao "
"amaldicoar ninguem por acidente."),
"rank_req":None ,
"color":"MAGENTA",
"passive_bonus":{"voice_power":1.0 ,"will_save_bonus":1.0 },
"extensions":[
{"name":"Pare!","desc":"Impede o alvo de agir por 1 turno.","ce_cost":15 ,"type":"stun","duration":1 },
{"name":"Ajoelhe-se!","desc":"Forca o corpo do alvo a se curvar, quebrando a guarda por completo.",
"ce_cost":22 ,"type":"attack","dmg_mult":0.8 ,"throat_dmg":3 ,
"debuff_def_pct":0.35 ,"debuff_duration":2 },
{"name":"Sangre!","desc":"Faz o alvo sangrar.","ce_cost":20 ,"type":"debuff_dot","dmg_mult":1.0 ,"duration":3 },
{"name":"Exploda!","desc":"Comando letal: explode o alvo por dentro.","ce_cost":50 ,"type":"attack","dmg_mult":3.0 ,"throat_dmg":5 },
{"name":"Durma!","desc":"Adormece o alvo por 2 turnos.","ce_cost":30 ,"type":"sleep","duration":2 },
{"name":"Morra!","desc":"O comando supremo, reservado para inimigos que realmente precisam morrer. Dano massivo.",
"ce_cost":90 ,"type":"attack","dmg_mult":5.0 ,"throat_dmg":25 },
],
"domain":None ,
},

"Boogie Woogie":{
"weight":4 ,
"desc":("Tecnica de Aoi Todo, ativada com uma palma de maos. Troca instantaneamente a posicao de dois "
"alvos que ele tocou com CE - permite fechar distancia num piscar de olhos, jogar um aliado pra "
"longe do perigo, ou trocar um inimigo direto no meio de um ataque devastador. "
"Passiva Ritmo de Combate: cada uso da +15% esquiva e +15% critico por 2 turnos, "
"inimigo trocado recebe -20% precisao por 2 turnos."),
"rank_req":None ,
"color":"YELLOW",
"passive_bonus":{"combo_bonus":1.0 ,"initiative":1.3 },
"extensions":[
{"name":"Boogie Woogie","desc":"Troca com inimigo. Inimigo perde proximo turno. +15% esquiva/crit 2t.",
"ce_cost":12 ,"type":"swap","stun_turns":1 ,"self_buff_dodge":0.15 ,
"self_buff_crit":0.15 ,"self_buff_duration":2 },
{"name":"Boogie Woogie: Ally Swap","desc":"Troca aliado com inimigo. Inimigo stun 1t, aliado +20% esquiva 1t.",
"ce_cost":15 ,"type":"swap_protect","stun_turns":1 ,"ally_dodge_bonus":0.20 },
{"name":"Fake Clap","desc":"Finge palmas. 60% stun 2t. Se ja foi trocado: dano 2.5x em vez de 1.5x.",
"ce_cost":18 ,"type":"stun_chance","dmg_mult":1.5 ,"stun_chance":0.60 ,"stun_turns":2 ,
"bonus_if_swapped_mult":2.5 },
{"name":"Boogie Combo","desc":"Troca repetidamente. 4x dano, sangra 3t, nao pode esquivar.",
"ce_cost":35 ,"type":"attack","dmg_mult":4.0 ,"bleed":True ,"bleed_turns":3 ,
"cant_dodge":True ,"self_buff_dodge":0.15 ,"self_buff_crit":0.15 ,"self_buff_duration":2 },
{"name":"Todo's Beatdown","desc":"Combo fisico pesado. 6x dano. +50% se foi trocado nos 3 ultimos turnos. 35% Black Flash.",
"ce_cost":50 ,"type":"attack","dmg_mult":6.0 ,"bonus_if_swapped_mult":1.5 ,
"black_flash_chance":0.35 ,"self_buff_dodge":0.15 ,"self_buff_crit":0.15 ,"self_buff_duration":2 },
],
"domain":None ,
},

"Idle Transfiguration":{
"weight":1 ,
"desc":("Tecnica de Mahito. Remodela a alma por toque. "
"v1.4.5: Passiva Forma da Alma - +35% resist dano fisico, +50% resist bleed/burn/poison, "
"cura 5% HP maximo por ataque de alma, marca Alma Distorcida."),
"rank_req":None ,
"color":"BRIGHT_MAGENTA",
"passive_bonus":{"soul_touch":1.0 ,"ignore_armor":0.5 },
"extensions":[
{"name":"Idle Transfiguration","desc":"Ataque de alma. 2.8x dano, ignora def, marca Alma Distorcida 3t (+20% dano seguinte).",
"ce_cost":25 ,"type":"attack","dmg_mult":2.8 ,"armor_pierce":True ,"soul_attack":True ,
"applies_soul_mark":3 },
{"name":"Body Repel","desc":"Alma em area. 3.5x AOE, 40% stun 2t.",
"ce_cost":30 ,"type":"attack_aoe","dmg_mult":3.5 ,"armor_pierce":True ,"soul_attack":True ,
"stun_chance":0.40 ,"stun_turns":2 },
{"name":"Soul Multiplicity","desc":"4.5x dano. Consome marcas de alma: +1x por marca. 3 marcas = stun 3t.",
"ce_cost":40 ,"type":"attack","dmg_mult":4.5 ,"armor_pierce":True ,"soul_attack":True ,
"consumes_soul_marks":True ,"stun_if_3_marks_turns":3 },
{"name":"Polymorphic Soul Isomer","desc":"6x dano, ignora def, sangra 4t, -30% def inimigo 3t.",
"ce_cost":55 ,"type":"attack","dmg_mult":6.0 ,"armor_pierce":True ,"soul_attack":True ,
"bleed":True ,"bleed_turns":4 ,"debuff_def_pct":0.30 ,"debuff_duration":3 },
{"name":"Self-Embodiment of Perfection","desc":"Expansao de dominio. Ataques de alma garantidos, "
"Alma Distorcida em todos/turno, inimigos com 3 marcas stunados. Custo: 80 CE + 50 CE/turno.",
"ce_cost":80 ,"type":"domain_active","domain_id":"self_embodiment",
"ce_per_turn":50 ,"hp_cost":0 ,
"dmg_per_turn_min":80 ,"dmg_per_turn_max":160 ,
"bleed_per_turn":2 ,"applies_soul_mark_per_turn":1 },
],
"domain":"Self-Embodiment of Perfection",
},

"Projection Sorcery":{
"weight":4 ,
"desc":("Tecnica do cla Zenin. Divide o movimento em 24 frames por segundo. "
"v1.4.5: Passiva 24 Frames - +40% velocidade, +25% esquiva. Esquivar da 1 Frame Stack (max 5). "
"Cada Frame Stack: +10% dano tecnicas."),
"rank_req":None ,
"color":"BRIGHT_YELLOW",
"passive_bonus":{"speed":1.4 ,"frame_freeze_chance":0.3 },
"extensions":[
{"name":"Projection Sorcery","desc":"2.2x dano. Aplica 1 Frame Lock. 3 locks = stun 2t.",
"ce_cost":20 ,"type":"attack","dmg_mult":2.2 ,"applies_frame_lock":1 ,
"stun_if_3_locks_turns":2 },
{"name":"Frame Technique","desc":"3x dano. Aplica 2 Frame Locks, -30% velocidade inimigo 3t.",
"ce_cost":28 ,"type":"attack","dmg_mult":3.0 ,"applies_frame_lock":2 ,
"debuff_speed_pct":0.30 ,"debuff_duration":3 },
{"name":"Speed Blitz","desc":"4.5x dano, nao pode esquivar. Consome Frame Stacks: +0.5x por stack. Stun 3t se 3 locks.",
"ce_cost":40 ,"type":"attack","dmg_mult":4.5 ,"cant_dodge":True ,
"consumes_frame_stacks":True ,"bonus_per_stack":0.5 ,
"stun_if_3_locks_turns":3 },
{"name":"Frame Freeze","desc":"2x AOE. Aplica 2 Frame Locks em todos, -25% esquiva 3t. Stun 2t se 3+ locks.",
"ce_cost":45 ,"type":"attack_aoe","dmg_mult":2.0 ,"applies_frame_lock":2 ,
"debuff_dodge_pct":0.25 ,"debuff_duration":3 ,"stun_if_3_locks_turns":2 },
{"name":"Time Cell Moon Palace","desc":"Expansao de dominio. +1 Frame Lock/turno em todos, "
"3 locks = congelado, +1 Frame Stack/turno, ataques certeiros em congelados. "
"Custo: 70 CE + 35 CE/turno.",
"ce_cost":70 ,"type":"domain_active","domain_id":"time_cell_moon_palace",
"ce_per_turn":35 ,"hp_cost":0 ,
"frame_lock_per_turn":1 ,"freeze_at_locks":3 ,
"dmg_per_turn_min":40 ,"dmg_per_turn_max":100 },
],
"domain":"Time Cell Moon Palace",
},

"Straw Doll Technique":{
"weight":4 ,
"desc":("Tecnica de Nobara Kugisaki, baseada em ritual xintoista antigo. Ela crava pregos amaldicoados "
"em um boneco de palha ligado ao alvo por um pedaco dele (cabelo, unha, sangue) - cada prego "
"cravado no boneco fere o alvo de verdade, onde quer que ele esteja. Os pregos vao se acumulando "
"como marcas no boneco ate serem descarregados na Ressonancia. Se ela consegue firmar o Vinculo "
"do Boneco logo no inicio da luta, cada prego seguinte crava com o dobro de forca, e a Ressonancia "
"pode ser reativada quantas vezes quiser sem gastar mais nenhuma Parte do Alvo - o mesmo ritual "
"que a consagrou como uma das feiticeiras mais letais da sua geracao."),
"rank_req":None ,
"color":"BRIGHT_RED",
"passive_bonus":{"ritual_bonus":1.0 ,"nail_precision":1.0 },
"extensions":[
{"name":"Vinculo do Boneco","desc":"Usa uma Parte do Alvo para firmar um vinculo permanente entre ele e o "
"boneco de palha por toda a batalha. Depois disso, todo prego crava com forca dobrada e a Ressonancia "
"fica liberada sem custo adicional de itens.",
"ce_cost":25 ,"type":"attack","dmg_mult":1.0 ,"requires_part":True ,"applies_bond":True },
{"name":"Prego Amaldicoado","desc":"Arremessa um prego carregado de CE contra o boneco de palha, cravando "
"mais uma marca nele - e na pele do alvo, a distancia.",
"ce_cost":14 ,"type":"attack","dmg_mult":1.6 ,"applies_nail_mark":1 },
{"name":"Martelada Kugisaki","desc":"Martela o prego direto no boneco com forca total. Corpo a corpo, "
"cru e pessoal - do jeito que Nobara prefere lutar.",
"ce_cost":20 ,"type":"attack","dmg_mult":2.1 ,"applies_nail_mark":1 },
{"name":"Hairpin","desc":"Chuta um prego com uma etiqueta explosiva de CE grudada - a jogada de abertura "
"favorita de Nobara, projetada para pegar o inimigo de surpresa com uma explosao em area.",
"ce_cost":30 ,"type":"attack_aoe","dmg_mult":2.6 ,"stun_chance":0.30 ,"stun_turns":1 },
{"name":"Saco de Cabelos (Hairbag)","desc":"Prepara efigies extras com fios de cabelo do alvo, amplificando "
"o proximo golpe de Ressonancia.",
"ce_cost":22 ,"type":"buff","buff":"resonance_mult","buff_value":50 ,"duration":3 },
{"name":"Ressonancia","desc":"O golpe definitivo. Descarrega de uma vez todos os pregos acumulados no "
"boneco de palha - quanto mais pregos cravados antes, mais devastador o resultado. Sem Vinculo do "
"Boneco ativo, precisa de uma Parte do Alvo a cada uso; com o vinculo firmado, pode ser reativada "
"livremente.",
"ce_cost":45 ,"type":"attack","dmg_mult":3.2 ,"requires_part":True ,"resonance_skill":True ,
"consumes_nail_marks":True ,"bonus_per_nail_mark":0.40 ,"stun_if_3_nails_turns":1 },
],
"domain":None ,
},

"Construcao":{
"weight":3 ,
"desc":"Tecnica rara que materializa objetos de CE pre-configurados.",
"rank_req":None ,
"color":"BRIGHT_BLUE",
"passive_bonus":{"construction_power":1.0 ,"no_fatigue":0.5 },
"extensions":[
{"name":"Pistola de CE","desc":"Constroi arma de fogo espiritual.","ce_cost":15 ,"type":"attack","dmg_mult":1.6 },
{"name":"Espada de CE","desc":"Constroi lamina: +dano por 3 turnos.","ce_cost":22 ,"type":"buff_weapon"},
{"name":"Escudo de CE","desc":"Reduz dano em 60% por 2 turnos.","ce_cost":25 ,"type":"buff_def","duration":2 },
{"name":"Canhao Astral","desc":"Construcao massiva: laser de CE.","ce_cost":70 ,"type":"attack","dmg_mult":3.8 },
],
"domain":None ,
},

"Manipulacao de Madeira (Cursed Wood)":{
"weight":3 ,
"desc":"Manipula madeira amaldicoada: brotos, espinhos e arvores vivas.",
"rank_req":None ,
"color":"GREEN",
"passive_bonus":{"nature_power":1.0 ,"regen_ally":1.0 },
"extensions":[
{"name":"Espinhos de Madeira","desc":"Espinhos brotam do chao perfurando o alvo.","ce_cost":15 ,"type":"attack","dmg_mult":1.5 },
{"name":"Prisao de Raizes","desc":"Tranca o alvo em raizes: stun 1 turno.","ce_cost":22 ,"type":"stun","duration":1 },
{"name":"Cura Natural","desc":"Cura aliado usando seiva amaldicoada.","ce_cost":28 ,"type":"heal_ally","heal_pct":0.25 },
{"name":"Arvore Carnivora","desc":"Invoca arvore que devora o inimigo.","ce_cost":50 ,"type":"attack","dmg_mult":3.2 },
],
"domain":None ,
},

"Bombardeiro de Sombra (Cursed Bombs)":{
"weight":3 ,
"desc":"Cria e detona bombas de CE em qualquer ponto visivel.",
"rank_req":None ,
"color":"BRIGHT_YELLOW",
"passive_bonus":{"aoe_power":1.0 ,"blast_radius":1.0 },
"extensions":[
{"name":"Bomba de Proximidade","desc":"Planta bomba que explode no proximo turno.","ce_cost":18 ,"type":"trap","dmg_mult":1.8 },
{"name":"Chuva de Bombas","desc":"Detona multiplas bombas em area.","ce_cost":35 ,"type":"attack_aoe","dmg_mult":2.2 },
{"name":"Bomba Teleguiada","desc":"Bomba que persegue o alvo.","ce_cost":30 ,"type":"attack","dmg_mult":2.3 ,"homing":True },
{"name":"Kamikaze Final","desc":"Suicidio explosivo: dano colossal em troca de HP.","ce_cost":80 ,"type":"attack_aoe","dmg_mult":5.0 ,"self_dmg_pct":0.50 },
],
"domain":None ,
},

"Canto Negromante (Necrocanto)":{
"weight":2 ,
"desc":"Manipula espiritos mortos: invocacao e maldicoes de longa duracao.",
"rank_req":None ,
"color":"BRIGHT_BLACK",
"passive_bonus":{"spirit_power":1.0 ,"death_save":1.0 },
"extensions":[
{"name":"Espectro Lacaio","desc":"Invoca espectro que ataca por 3 turnos.","ce_cost":20 ,"type":"summon","summon_id":"specter","duration":3 },
{"name":"Coro dos Mortos","desc":"Espectros atormentam o alvo: DOT + reducao de defesa.","ce_cost":30 ,"type":"debuff_dot","dmg_mult":1.3 ,"duration":3 },
{"name":"Requiem","desc":"Drena vida do alvo para voce.","ce_cost":35 ,"type":"lifesteal","dmg_mult":1.8 ,"lifesteal_pct":0.6 },
{"name":"Morte Vindas","desc":"Chance de matar instantaneamente abaixo de 30% HP.","ce_cost":75 ,"type":"attack","dmg_mult":3.5 ,"instakill_below_pct":0.30 },
],
"domain":None ,
},

"Cristais de CE (Cursed Crystal)":{
"weight":2 ,
"desc":"Cristaliza CE em estruturas cortantes, barreiras e armadilhas.",
"rank_req":None ,
"color":"BRIGHT_CYAN",
"passive_bonus":{"crystal_power":1.0 ,"barrier_strength":1.0 },
"extensions":[
{"name":"Lanca de Cristal","desc":"Dispara cristal perfurante.","ce_cost":14 ,"type":"attack","dmg_mult":1.5 ,"armor_pierce":True },
{"name":"Barreira de Cristal","desc":"Barreira fisica que bloqueia 70% do dano.","ce_cost":25 ,"type":"buff_def","duration":2 },
{"name":"Chuva Cristalina","desc":"Cristais caem em area.","ce_cost":35 ,"type":"attack_aoe","dmg_mult":2.0 },
{"name":"Prisao de Cristal Eterno","desc":"Crystaliza o inimigo: stun por 2 turnos.","ce_cost":50 ,"type":"stun","duration":2 },
{"name":"Cathedral of Crystals","desc":"EXPANSAO DE DOMINIO ATIVA. Catedral de cristais onde cada faceta corta. "
"Certeiro em todos inimigos, sangramento 3 stacks/turno, dano 60-150/turno. "
"Custo: 70 CE + 35 CE/turno. Dura ate CE acabar.",
"ce_cost":70 ,"type":"domain_active","domain_id":"cathedral_of_crystals",
"ce_per_turn":35 ,"dmg_per_turn_min":60 ,"dmg_per_turn_max":150 ,
"bleed_per_turn":3 },
],
"domain":"Cathedral of Crystals",
},

"Disco Maldito (Cursed Disk)":{
"weight":2 ,
"desc":"Cria discos cortantes de CE que podem ricochetear.",
"rank_req":None ,
"color":"BRIGHT_MAGENTA",
"passive_bonus":{"ricochet":1.0 ,"cut_power":1.0 },
"extensions":[
{"name":"Disco Unico","desc":"Arremeca disco cortante.","ce_cost":12 ,"type":"attack","dmg_mult":1.4 },
{"name":"Ricochete Triplo","desc":"Disco que pula entre 3 alvos.","ce_cost":28 ,"type":"attack_chain","dmg_mult":1.2 ,"hits":3 },
{"name":"Vortex de Discos","desc":"Discos giram ao redor do alvo: DOT.","ce_cost":30 ,"type":"debuff_dot","dmg_mult":1.0 ,"duration":3 },
{"name":"Serra Infinita","desc":"Disco gigante que corta tudo no caminho.","ce_cost":60 ,"type":"attack_aoe","dmg_mult":3.0 },
],
"domain":None ,
},

"Garra Amaldiçoada":{
"weight":5 ,
"desc":"Garras de CE que crescem das maos.",
"rank_req":None ,
"color":"BRIGHT_RED",
"passive_bonus":{"physical_bonus":1.2 ,"bleed_chance":0.3 },
"extensions":[
{"name":"Corte Vertical","desc":"Garras cortam de cima a baixo.","ce_cost":12 ,"type":"attack","dmg_mult":1.6 },
{"name":"Garra Rapida","desc":"Cinco cortes horizontais em sequencia.","ce_cost":18 ,"type":"attack","dmg_mult":1.8 ,"hits":3 },
{"name":"Garra das Sombras","desc":"Garras invisiveis: ignoram armadura.","ce_cost":25 ,"type":"attack","dmg_mult":2.0 ,"armor_pierce":True },
{"name":"Corte Transversal","desc":"Corte que atravessa o alvo: dano massivo + bleed.","ce_cost":40 ,"type":"attack","dmg_mult":3.0 ,"bleed":True },
],
"domain":None ,
},

"Cleave and Dismantle (Sukuna)":{
"weight":0 ,
"desc":("Tecnica do Rei das Maldicoes. NAO EVOLUI POR XP - evolui por DEDOS ingeridos. "
"Stages: 1 dedo (Dismantle+Cleave), 6 dedos (Spiderweb Cut), 7 dedos (Fire Arrow), "
"8 dedos (World Cutting Slash), 12 dedos (Incomplete Malevolent Shrine), "
"18 dedos (Malevolent Shrine completo). "
"Cada dedo: +10% dano, +5% chance de Sukuna controlar, -8 CE custo, -10% dano recebido."),
"rank_req":None ,
"color":"BRIGHT_RED",
"passive_bonus":{"physical_bonus":1.5 ,"ce_efficiency":1.2 },
"extensions":[

{"name":"Dismantle","desc":"Corte conceitual. 2.2x dano, ignora 15% def. Escala com dedos.",
"ce_cost":20 ,"type":"attack","dmg_mult":2.2 ,"sukuna_skill":True ,
"requires_min_fingers":1 ,"armor_pierce_pct_dynamic":True },
{"name":"Cleave","desc":"Corte que se ajusta a resistencia. 2.8x dano, ignora 30% def. Mais dano em HP alto.",
"ce_cost":30 ,"type":"attack","dmg_mult":2.8 ,"sukuna_skill":True ,
"requires_min_fingers":1 ,"armor_pierce_pct_dynamic":True ,"bonus_vs_high_hp":True },

{"name":"Spiderweb Cut","desc":"Cortes em teia em todos. 2.5x AOE, sangra 2t.",
"ce_cost":45 ,"type":"attack_aoe","dmg_mult":2.5 ,"sukuna_skill":True ,
"requires_min_fingers":6 ,"bleed":True ,"bleed_turns":2 },

{"name":"Open: Fire Arrow","desc":"Flecha de fogo amaldicoado. 3.5x AOE, queimadura 3t. Bonus em queimando.",
"ce_cost":65 ,"type":"attack_aoe","dmg_mult":3.5 ,"sukuna_skill":True ,
"requires_min_fingers":7 ,"burn":True ,"burn_turns":3 ,"bonus_vs_burning":True },

{"name":"World Cutting Slash","desc":"Corte que divide o mundo. 40x dano, ignora 70% def, atravessa Infinito, carga 1t, 1 uso/luta.",
"ce_cost":90 ,"type":"attack","dmg_mult":40.0 ,"sukuna_skill":True ,
"requires_min_fingers":8 ,"armor_pierce_pct_dynamic":True ,
"infinity_bypass":True ,
"cant_dodge":True ,"charge_turns":1 ,"one_use_per_battle":True },

{"name":"Incomplete Malevolent Shrine","desc":"Expansao INCOMPLETA. Certeiro em todos, Dismantle/Cleave AOE, "
"sangramento/turno, dano 200-600/turno. Custo: 82 CE + 45 CE/turno.",
"ce_cost":82 ,"type":"domain_active","domain_id":"incomplete_malevolent_shrine",
"requires_min_fingers":12 ,"ce_per_turn":45 ,"dmg_per_turn_min":200 ,"dmg_per_turn_max":600 ,
"bleed_per_turn":2 },

{"name":"Malevolent Shrine","desc":"EXPANSAO COMPLETA. Certeiro em todos, dano 800-1100/turno. "
"Custo: 82 CE + 25 CE/turno.",
"ce_cost":82 ,"type":"domain_active","domain_id":"malevolent_shrine",
"requires_min_fingers":18 ,"ce_per_turn":25 ,"dmg_per_turn_min":800 ,"dmg_per_turn_max":1100 },
],
"domain":"Malevolent Shrine",
"sukuna_only":True ,
},

"Rika (Yuta Okkotsu)":{
"weight":0 ,
"desc":("Yuta Okkotsu, quando crianca, fez um voto de amor com o espirito de sua amiga de infancia "
"Rika Orimoto apos ela morrer tragicamente. Esse voto a transformou em 'Rika', o espirito amaldicoado "
"mais forte que ja existiu - uma entidade colossal e espectral que so se manifesta em forca total "
"quando Yuta esta em perigo real ou dominado pela emocao. Quanto mais desesperado ele fica, mais "
"Rika 'sente' e mais devastador o poder liberado. Yuta tambem herdou de Suguru Geto a capacidade "
"de copiar qualquer tecnica amaldicoada que testemunhe de perto, replicando-a com precisao quase "
"perfeita (foi assim que ele copiou a Idle Transfiguration de Mahito)."),
"rank_req":None ,
"color":"BRIGHT_MAGENTA",
"passive_bonus":{"physical_bonus":1.4 ,"ce_efficiency":1.5 },
"extensions":[
{"name":"Play Cool","desc":"Um corte rapido com a katana Play Cool, a primeira das duas lâminas amaldicoadas "
"de Yuta. Simples, preciso, mortal.",
"ce_cost":20 ,"type":"attack","dmg_mult":1.8 },
{"name":"Play Cool e Sukiyaki: Corte Duplo","desc":"Yuta desembainha as duas katanas (Play Cool e Sukiyaki) "
"e ataca em sequencia fluida, um golpe guiando o outro.",
"ce_cost":38 ,"type":"attack","dmg_mult":1.9 ,"hits":2 ,"bleed":True ,"bleed_turns":2 },
{"name":"Copia Amaldicoada","desc":"Observa de perto e copia com precisao a tecnica do alvo - a mesma "
"habilidade que permitiu a Yuta copiar a Idle Transfiguration de Mahito. Funciona ate contra adaptacoes: "
"se o alvo se adapta a golpes como Mahoraga, Yuta consegue copiar isso tambem. So que manter a copia "
"funcionando exige uma quantidade absurda de CE a cada uso.",
"ce_cost":40 ,"type":"copy_technique","dmg_mult":2.0 ,"copy_ce_cost":180 },
{"name":"Invocar Rika (Incompleta)","desc":"Chama Rika para lutar ao seu lado em forma parcial - uma "
"manifestacao instavel, mas ainda assim capaz de golpes devastadores por conta propria. Ela ataca com "
"seu proprio moveset a cada turno, sem depender das ordens de Yuta.",
"ce_cost":50 ,"type":"summon_rika","rika_form":"incomplete"},
{"name":"Invocar Rika (Completa)","desc":"Yuta abre mao de quase toda contencao para trazer Rika em forma "
"quase completa - muito mais forte que a versao incompleta, mas manter essa manifestacao ativa drena "
"uma quantidade absurda de CE a cada turno.",
"ce_cost":90 ,"type":"summon_rika","rika_form":"complete"},
{"name":"Rika Desperta: Braco Espectral","desc":"Rika se manifesta parcialmente atras de Yuta, um braco "
"espectral gigante esmagando o alvo. Quanto mais perto da morte Yuta estiver, mais forte e o golpe - "
"Rika sente o desespero dele e responde com fúria crescente.",
"ce_cost":45 ,"type":"attack","dmg_mult":2.8 ,"bleed":True ,"bleed_turns":4 ,
"scales_with_missing_hp":True ,"rage_mult":1.8 },
{"name":"Voto de Rika: Reversao Amaldicoada","desc":"O vinculo entre Yuta e Rika restaura parte da vida "
"perdida - o mesmo laco de amor e vinganca que trouxe Rika de volta continua protegendo Yuta.",
"ce_cost":30 ,"type":"heal","heal_pct":0.28 },
{"name":"Invocacao de Rika: Trovao Amaldicoado","desc":"Yuta clama por Rika e ela responde por completo, "
"mesmo fora do dominio - um pilar de raio amaldicoado roxo-escuro desce do ceu e varre tudo em seu "
"caminho, a mesma cena que reduziu um exercito inteiro de clones de Geto a cinzas em Shibuya. "
"So pode ser conjurado uma vez por batalha.",
"ce_cost":90 ,"type":"attack","dmg_mult":7.0 ,"armor_pierce_pct":0.30 ,"stun_chance":0.5 ,"stun_turns":2 ,
"scales_with_missing_hp":True ,"rage_mult":1.2 ,"one_use_per_battle":True },
{"name":"Cursed Womb: Straw Doll Technique","desc":"EXPANSAO DE DOMINIO ATIVA. Rika abandona toda contencao "
"e se manifesta em forma completa - um titã espectral colossal com contornos de boneco de palha, "
"capaz de devorar qualquer coisa em seu caminho. Certeiro em todos, dano 300-700/turno. "
"Custo: 80 CE + 45 CE/turno.",
"ce_cost":80 ,"type":"domain_active","domain_id":"cursed_womb",
"ce_per_turn":45 ,"dmg_per_turn_min":300 ,"dmg_per_turn_max":700 ,"bleed_per_turn":2 },
],
"domain":"Cursed Womb: Straw Doll Technique",
},

"Ittadakimasu (Hakari Kinji)":{
"weight":0 ,
"desc":("Hakari Kinji fez um contrato amaldicoado com uma entidade desconhecida: em troca de poder de "
"combate absurdo, ele deve constantemente 'apostar' - pagando parte de sua propria sorte e vida a "
"cada golpe. Sua tecnica, Ittadakimasu ('vou receber'), funciona como uma maquina caca-niqueis: cada "
"ataque saca uma carta simbolica, e cartas de risco alto podem tanto amplificar seu poder de forma "
"absurda quanto desperdicar a jogada. Essa incerteza culmina no lendario Star Rage, o soco mais forte "
"que Hakari consegue desferir quando toda a sorte acumulada se converte em um unico golpe."),
"rank_req":None ,
"color":"BRIGHT_YELLOW",
"passive_bonus":{"physical_bonus":1.6 ,"ce_efficiency":1.1 },
"extensions":[
{"name":"Ittadakimasu","desc":"Encosta no alvo e 'recebe' parte da energia vital dele como pagamento do "
"contrato amaldicoado. Cada toque alimenta a proxima aposta.",
"ce_cost":35 ,"type":"lifesteal","dmg_mult":2.2 ,"lifesteal_pct":0.5 },
{"name":"Idle Death Gamble: Carta Numerica","desc":"Um golpe direto e confiavel - a aposta mais segura da "
"maquina, sem grandes riscos nem grandes premios.",
"ce_cost":22 ,"type":"attack","dmg_mult":2.0 },
{"name":"Idle Death Gamble: Joker","desc":"A carta mais arriscada da maquina. Cinquenta por cento de chance "
"de dano absurdo, cinquenta por cento de desperdicar a jogada - pura sorte de cassino.",
"ce_cost":45 ,"type":"attack","dmg_mult":2.0 ,"gamble":True ,"gamble_win_chance":0.5 ,
"gamble_high_mult":3.2 ,"gamble_low_mult":0.6 ,"stun_chance":0.25 ,"stun_turns":1 },
{"name":"Reversal: Red Bull","desc":"Puxa uma carta de reversao - transforma o proprio infortunio acumulado "
"em uma sobrecarga momentanea de forca e velocidade.",
"ce_cost":30 ,"type":"buff","buff":"attack","buff_mult":1.35 ,"speed_mult":1.30 ,"duration":3 },
{"name":"Star Rage","desc":"O soco lendario de Hakari. Toda a sorte e energia acumuladas em suas apostas "
"se concentram em um unico golpe imparavel, capaz de derrubar feiticeiros de grau especial.",
"ce_cost":70 ,"type":"attack","dmg_mult":6.5 ,"armor_pierce_pct":0.25 },
{"name":"Domain Expansion: Private Pure Love Train","desc":"EXPANSAO DE DOMINIO ATIVA. Um trem amaldicoado "
"surge correndo por trilhos que nao existem, atropelando tudo em seu caminho sem chance de fuga - "
"a aposta final. O dominio de Hakari funciona como uma maquina caca-niqueis: ele gira ate 3 vezes "
"antes de quebrar, e se cair 7-7-7, o jackpot concede CE e HP infinitos para o resto da batalha. "
"Certeiro em todos, dano 350-750/turno. Custo: 80 CE + 45 CE/turno.",
"ce_cost":80 ,"type":"domain_active","domain_id":"private_pure_love_train",
"ce_per_turn":45 ,"dmg_per_turn_min":350 ,"dmg_per_turn_max":750 ,"stun_all_per_turn":True ,
"slot_machine":True ,"max_spins":3 ,"jackpot_chance_per_spin":0.08 },
],
"domain":"Private Pure Love Train",
},
}

BIRTH_TRAITS ={
"Nenhum Traço":{
"weight":50 ,
"desc":"Nenhuma passiva especial. Apenas determinacao.",
"effects":{},
},

"Seis Olhos (Six Eyes)":{
"weight":1 ,
"desc":("Traco rarissimo do cla Gojo. Percepcao extrema do fluxo de CE. "
"v1.4.5: -60% custo todas tecnicas, -75% custo Limitless, +100% regen CE, "
"+45% esquiva, +75% controle, ve invisiveis, -50% ambush, -35% stun/mental, "
"25% chance recuperar 20% CE gasto, +5% CE maximo ao defender/esquivar, +70% critico. "
"Sinergia Limitless: -75% consumo Infinito, Hollow Purple ignora +10% def, Max Blue/Red +25% dano."),
"effects":{
"ce_efficiency":2.5 ,
"control_bonus":1.75 ,
"dodge":1.45 ,
"see_through":True ,
"ce_regen":2.0 ,
"crit_chance_bonus":0.70 ,
"stun_resist":1.35 ,
"mental_resist":1.35 ,
"ambush_immunity":True ,
"first_strike_bonus":1.3 ,
},
"synergy":"Limitless",
},

"Corpo Perfeito (Sukuna Heian + Six Eyes)":{
"weight":0 ,
"desc":("O traco mais raro que existe. O corpo perfeito da era Heian, unido aos Seis Olhos. "
"Chance de nascimento: 0,10%. Corpo indestrutivel, CE quase infinito, reflexos absurdos, "
"instinto assassino de Sukuna e percepcao total dos Seis Olhos no mesmo hospedeiro."),
"effects":{
"ce_efficiency":4.0 ,
"control_bonus":2.5 ,
"dodge":2.0 ,
"crit_chance_bonus":0.30 ,
"counter_chance":0.35 ,
"physical_defense":2.0 ,
"stun_resist":1.85 ,
"lifesteal_pct":0.20 ,
"ce_max_bonus":3.0 ,
"hp_max_penalty":1.8 ,
"speed_bonus":1.6 ,
"see_through":True ,
"ce_regen":2.5 ,
},
"synergy":"Limitless",
},

"Afinidade de CE":{
"weight":10 ,
"desc":"Reduz custo de tecnicas e melhora eficiencia geral de CE.",
"effects":{
"ce_efficiency":1.4 ,
"ce_regen":1.2 ,
},
},
"Resistencia Espiritual":{
"weight":10 ,
"desc":"Reduz efeitos mentais, ilusoes e pressao amaldicoada.",
"effects":{
"mental_resist":1.5 ,
"curse_pressure_resist":1.4 ,
"stun_resist":1.3 ,
},
},
"Percepcao de Energia":{
"weight":10 ,
"desc":"Permite detectar inimigos e rastros ocultos.",
"effects":{
"detection_range":2.0 ,
"ambush_immunity":True ,
"first_strike_bonus":1.3 ,
},
},
"Instinto de Combate":{
"weight":8 ,
"desc":"Melhora reflexos automaticos e reacao em combate.",
"effects":{
"dodge":1.25 ,
"counter_chance":0.20 ,
"initiative":1.3 ,
},
},
"Corpo Adaptativo":{
"weight":6 ,
"desc":"Reduz penalidades de tecnicas dificeis de executar.",
"effects":{
"technique_mastery":1.5 ,
"fatigue_resist":1.4 ,
"rct_bonus":1.3 ,
},
},
"Pacto de Sangue Antigo":{
"weight":4 ,
"desc":"Um ancestral fez um pacto com maldicoes. Voce herda parte desse poder, mas paga o preco.",
"effects":{
"ce_max_bonus":1.5 ,
"power_bonus":1.2 ,
"karma_penalty":2.0 ,
"hp_max_penalty":0.85 ,
},
},
"Visao Amaldicoada":{
"weight":5 ,
"desc":"Ve CE bruta como cores. Identifica pontos fracos automaticamente.",
"effects":{
"crit_chance_bonus":0.15 ,
"weakpoint_detection":True ,
"ce_regen":1.1 ,
},
},
"Pele de Ferro Amaldicoado":{
"weight":5 ,
"desc":"Sua pele naturalmente repele CE fraca. Reduz dano fisico.",
"effects":{
"physical_defense":1.4 ,
"ce_resist":1.2 ,
},
},
"Sopro da Morte (Death Breath)":{
"weight":3 ,
"desc":"Seu toque drena vida levemente. Vampirismo natural.",
"effects":{
"lifesteal_pct":0.10 ,
"ce_drain_on_hit":2 ,
},
},
"Memoria Ancestral":{
"weight":4 ,
"desc":"Acesso a memorias de feiticeiros do passado. Aprende tecnicas mais rapido.",
"effects":{
"xp_bonus":1.3 ,
"skill_unlock_bonus":1.0 ,
},
},
"Feiticeiro Celestial (Restricao Menor)":{
"weight":3 ,
"desc":"Uma restricao parcial: perdeu um pouco de CE, mas ganhou corpo extraordinario.",
"effects":{
"physical_bonus":1.6 ,
"ce_max_penalty":0.7 ,
"speed_bonus":1.3 ,
},
},
"Marca do Carrasco":{
"weight":2 ,
"desc":"Sua presenca amedronta maldicoes. Mas elas te odeiam mais.",
"effects":{
"fear_aura":True ,
"aggro_mult":1.5 ,
"curse_aggression":1.5 ,
},
},
"Sorte de Sukuna":{
"weight":1 ,
"desc":"Voce nasceu sob uma estrela amaldicoada. Raro extremo. Eventos raros aparecem mais.",
"effects":{
"luck":2.0 ,
"rare_event_chance":1.5 ,
"sukuna_finger_find_chance":2.0 ,
},
},
}

DOMAINS ={
"Unlimited Void":{
"owner_technique":"Limitless",
"desc":("O vacuo infinito. Mostra tudo ao alvo de uma vez - sobrecarga total. "
"v1.4.5: Custo 70 CE/turno. Stun enquanto ativo, ataque garantido, "
"apos acabar: alvo fica parado 5 turnos e toma 50% da vida de dano."),
"effect":{
"sure_hit":True ,
"dmg_mult":2.0 ,
"duration":3 ,
"stun_target":1 ,
"ce_per_turn":70 ,
"post_duration_stun":5 ,
"post_duration_dmg_pct":0.50 ,
},
"ascii":"void",
},
"Chimera Shadow Garden":{
"owner_technique":"Dez Sombras",
"desc":"Um jardim de sombras onde todos os shikigamis podem atacar livremente.",
"effect":{
"sure_hit":True ,
"dmg_mult":1.8 ,
"duration":3 ,
"summon_all":True ,
},
"ascii":"shadow",
},
"Self-Embodiment of Perfection":{
"owner_technique":"Idle Transfiguration",
"desc":"O dominio da alma. Toque automatico - transfiguracao garantida.",
"effect":{
"sure_hit":True ,
"dmg_mult":2.0 ,
"duration":3 ,
"instakill_below_pct":0.20 ,
},
"ascii":"soul",
},
"Cathedral of Crystals":{
"owner_technique":"Cristais de CE",
"desc":"Uma catedral de cristais onde cada faceta corta.",
"effect":{
"sure_hit":True ,
"dmg_mult":1.9 ,
"duration":3 ,
"bleed_stacks":3 ,
},
"ascii":"crystal",
},
"Dominio Simples (Hollow Wicker Basket)":{
"owner_technique":None ,
"desc":"Um dominio defensivo que neutraliza o efeito de sure-hit inimigo.",
"effect":{
"anti_domain":True ,
"neutralize_sure_hit":True ,
"duration":2 ,
"no_damage":True ,
},
"ascii":"wicker",
},
"Malevolent Shrine":{
"owner_technique":"Cleave and Dismantle (Sukuna)",
"desc":"O dominio do Rei das Maldicoes. Santuario aberto - cortes conceituais atingem TUDO.",
"effect":{
"sure_hit":True ,
"dmg_mult":2.5 ,
"duration":3 ,
"bleed_stacks":3 ,
"scales_with_fingers":True ,
},
"ascii":"shrine",
},
"Blood Domain":{
"owner_technique":"Manipulacao de Sangue",
"desc":"Dominio de sangue. Todos inimigos sangram por turno, usuario cura HP por turno.",
"effect":{
"sure_hit":True ,
"bleed_per_turn":3 ,
"heal_per_turn_pct":0.05 ,
"ce_per_turn":30 ,
"dmg_per_turn_min":30 ,
"dmg_per_turn_max":60 ,
},
"ascii":"blood",
},
"Time Cell Moon Palace":{
"owner_technique":"Projection Sorcery",
"desc":"Dominio do tempo. Todos inimigos recebem Frame Lock por turno, congelados com 3+ locks.",
"effect":{
"sure_hit":True ,
"frame_lock_per_turn":1 ,
"freeze_at_locks":3 ,
"frame_stack_per_turn":1 ,
"ce_per_turn":35 ,
},
"ascii":"time",
},
"Incomplete Malevolent Shrine":{
"owner_technique":"Cleave and Dismantle (Sukuna)",
"desc":"Versao incompleta do Malevolent Shrine. Dano 200-600 por turno.",
"effect":{
"sure_hit":True ,
"ce_per_turn":45 ,
"dmg_per_turn_min":200 ,
"dmg_per_turn_max":600 ,
"bleed_per_turn":2 ,
},
"ascii":"shrine",
},
"Cursed Womb: Straw Doll Technique":{
"owner_technique":"Rika (Yuta Okkotsu)",
"desc":"Rika se manifesta em forma completa - um titã espectral que devora tudo em seu caminho.",
"effect":{
"sure_hit":True ,
"dmg_mult":2.2 ,
"duration":3 ,
"ce_per_turn":45 ,
"dmg_per_turn_min":300 ,
"dmg_per_turn_max":700 ,
"bleed_per_turn":2 ,
},
"ascii":"rika",
},
"Private Pure Love Train":{
"owner_technique":"Ittadakimasu (Hakari Kinji)",
"desc":"Um trem amaldicoado corre por trilhos infinitos, atropelando tudo sem chance de fuga.",
"effect":{
"sure_hit":True ,
"dmg_mult":2.4 ,
"duration":3 ,
"ce_per_turn":45 ,
"dmg_per_turn_min":350 ,
"dmg_per_turn_max":750 ,
"stun_target":1 ,
},
"ascii":"train",
},
"Trono do Vazio Carmesim":{
"owner_technique":"Heitor Careca",
"desc":"A fusao impossivel entre o vazio infinito e o santuario maldito. Nem espaco nem conceito escapam.",
"effect":{
"sure_hit":True ,
"dmg_mult":4.0 ,
"duration":4 ,
"ce_per_turn":60 ,
"dmg_per_turn_min":600 ,
"dmg_per_turn_max":1400 ,
"bleed_stacks":6 ,
"stun_target":1 ,
},
"ascii":"throne",
},
}

def roll_innate_technique ():

    eligible ={name :data for name ,data in INNATE_TECHNIQUES .items ()
    if data .get ("weight",0 )>0 }
    total =sum (t ["weight"]for t in eligible .values ())
    if total <=0 :
        return "Sem Tecnica"
    roll =random .randint (1 ,total )
    current =0 
    for name ,data in eligible .items ():
        current +=data ["weight"]
        if roll <=current :
            return name 
    return "Sem Tecnica"

PERFECT_BODY_TRAIT_NAME ="Corpo Perfeito (Sukuna Heian + Six Eyes)"
PERFECT_BODY_CHANCE =0.001 

def roll_birth_trait ():

    if random .random ()<PERFECT_BODY_CHANCE :
        return PERFECT_BODY_TRAIT_NAME 
    total =sum (t ["weight"]for t in BIRTH_TRAITS .values ())
    roll =random .randint (1 ,total )
    current =0 
    for name ,data in BIRTH_TRAITS .items ():
        current +=data ["weight"]
        if roll <=current :
            return name 
    return "Nenhum Traço"

def roll_heavenly_restriction ():

    return random .randint (1 ,100 )==1 

def can_use_rct (player ):

    if player .level_system .level <10 :
        return False 
    if player .attributes .get ("controle",0 )<15 :
        return False 
    return True 

def get_rct_info ():
    return {
    "name":"Tecnica Reversa (RCT)",
    "desc":"Inverte o fluxo de CE para curar. Consome muita energia.",
    "ce_cost":60 ,
    "heal_pct":0.40 ,
    "exhaustion_turns":1 ,
    }

def get_technique (name ):
    return INNATE_TECHNIQUES .get (name )

def get_trait (name ):
    return BIRTH_TRAITS .get (name )

def get_domain (name ):
    return DOMAINS .get (name )

def get_technique_color (name ):
    t =INNATE_TECHNIQUES .get (name )
    if not t :
        return "BRIGHT_WHITE"
    return t .get ("color","BRIGHT_WHITE")

def list_techniques_for_display ():
    out =[]
    for name ,data in INNATE_TECHNIQUES .items ():
        out .append ({
        "name":name ,
        "weight":data ["weight"],
        "desc":data ["desc"],
        "domain":data .get ("domain"),
        })
    return out 

def list_traits_for_display ():
    out =[]
    for name ,data in BIRTH_TRAITS .items ():
        out .append ({
        "name":name ,
        "weight":data ["weight"],
        "desc":data ["desc"],
        })
    return out 

def get_available_extensions (player ):

    tech_name =player .innate_technique 
    if player .sukuna_mastered and tech_name !="Cleave and Dismantle (Sukuna)":

        techs =[tech_name ,"Cleave and Dismantle (Sukuna)"]
    else :
        techs =[tech_name ]

    available =[]
    for tn in techs :
        tech =INNATE_TECHNIQUES .get (tn )
        if not tech :
            continue 
        for ext in tech .get ("extensions",[]):

            req_stage =ext .get ("requires_stage")
            if req_stage :
                if player ._get_technique_stage ()!=req_stage and tn =="Limitless":
                    continue 

            req_fingers =ext .get ("requires_min_fingers",0 )
            if req_fingers >0 and player .sukuna_fingers_eaten <req_fingers :
                continue 
            available .append ((tn ,ext ))
    return available 

TECHNIQUE_ROULETTE_COST =6000 
TRAIT_ROULETTE_COST =3800 

def roulette_innate_technique (player ,ui_module =None ):

    if player .money <TECHNIQUE_ROULETTE_COST :
        if ui_module :
            ui_module .tprint (c (f"\nIenes insuficientes! Custo: {TECHNIQUE_ROULETTE_COST }",Color .RED ))
            ui_module .pause ()
        return False 
    old_tech =player .innate_technique 
    new_tech =roll_innate_technique ()
    attempts =0 
    while new_tech ==old_tech and attempts <5 :
        new_tech =roll_innate_technique ()
        attempts +=1 
    player .money -=TECHNIQUE_ROULETTE_COST 
    player .technique_roulette_count +=1 
    player .innate_technique =new_tech 
    player .technique_xp =0 
    player .technique_level =1 
    player .recalculate_derived ()
    if ui_module :
        tech =INNATE_TECHNIQUES [new_tech ]
        ui_module .tprint (c ("\n!! ROLETA DE TECNICA INATA !!",Color .BRIGHT_MAGENTA +Color .BOLD ))
        ui_module .tprint (c (f"Tecnica anterior: {old_tech }",Color .DIM ))
        ui_module .tprint (c (f"Nova tecnica: {new_tech }",Color .BRIGHT_MAGENTA +Color .BOLD ))
        ui_module .tprint (tech ["desc"])
        ui_module .tprint (c (f"-{TECHNIQUE_ROULETTE_COST } ienes",Color .YELLOW ))
        ui_module .pause ()
    return True 

def roulette_birth_trait (player ,ui_module =None ):

    if player .money <TRAIT_ROULETTE_COST :
        if ui_module :
            ui_module .tprint (c (f"\nIenes insuficientes! Custo: {TRAIT_ROULETTE_COST }",Color .RED ))
            ui_module .pause ()
        return False 
    old_trait =player .birth_trait 
    new_trait =roll_birth_trait ()
    attempts =0 
    while new_trait ==old_trait and attempts <5 :
        new_trait =roll_birth_trait ()
        attempts +=1 
    player .money -=TRAIT_ROULETTE_COST 
    player .trait_roulette_count +=1 
    player .birth_trait =new_trait 
    player .recalculate_derived ()
    if ui_module :
        trait =BIRTH_TRAITS [new_trait ]
        ui_module .tprint (c ("\n!! ROLETA DE TRACO DE NASCIMENTO !!",Color .BRIGHT_BLUE +Color .BOLD ))
        ui_module .tprint (c (f"Traco anterior: {old_trait }",Color .DIM ))
        ui_module .tprint (c (f"Novo traco: {new_trait }",Color .BRIGHT_BLUE +Color .BOLD ))
        ui_module .tprint (trait ["desc"])
        ui_module .tprint (c (f"-{TRAIT_ROULETTE_COST } ienes",Color .YELLOW ))
        ui_module .pause ()
    return True

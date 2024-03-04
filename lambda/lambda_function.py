#ME_ESCUTE_MQTT

MQTT_SERVIDOR           = "test.mosquitto.org"                                                          
MQTT_PORTA              = 1883			 			                
MQTT_TOPICO             = "tu7ZzJ17U8sfFtn2j1MUrao1jza2CBO53RxI6RecRvYz2W1erK"
MQTT_USUARIO            = ""
MQTT_SENHA              = ""

import paho.mqtt.publish as publish
import time
import random
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.slu.entityresolution.resolution import Resolution
from ask_sdk_model.slu.entityresolution import StatusCode
from ask_sdk_model import Response

def enviar(comando, dispositivo):
    if MQTT_USUARIO == "" and MQTT_SENHA == "":
        publish.single(MQTT_TOPICO, '{{"comando": "{0}", "dispositivo": "{1}"}}'.format(comando, dispositivo), hostname=MQTT_SERVIDOR, port=MQTT_PORTA)
    else:
        publish.single(MQTT_TOPICO, '{{"comando": "{0}", "dispositivo": "{1}"}}'.format(comando, dispositivo), hostname=MQTT_SERVIDOR, port=MQTT_PORTA, auth={'username':MQTT_USUARIO, 'password':MQTT_SENHA})

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
        
    def handle(self, handler_input):
        speak_output = random.choice([
            "Deseja algo?",
            "Pois não?",
            "Posso ajudar?",
            "Como posso ajudar?",
            "O que precisa?",
            "Estou ouvindo.",
            "Posso auxiliar?",
            "Estou à disposição.",
            "Como posso ser útil?",
            "O que deseja?",
            "Estou aqui."
        ])
        
        return (handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class intencaodecontinuidadeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("intencao_de_continuidade")(handler_input)
        
    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="comandos_de_continuidade")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    
                    enviar(resolution.values[0].value.name, handler_input.request_envelope.context.system.device.device_id)
                        
                    speak_output = random.choice([
                        "Algo mais?",
                        "Deseja algo mais?",
                        "Mais alguma coisa?",
                        "Deseja mais alguma coisa?",
                        "Algum outro desejo?",
                        "Alguma outra solicitação?",
                        "Algo adicional?",
                        "Tem mais algum pedido?"
                    ])
                else:
                    raise
                
        return (handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class intencaodiretaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("intencao_direta")(handler_input)
        
    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="comandos_diretos")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    
                    enviar(resolution.values[0].value.name, handler_input.request_envelope.context.system.device.device_id)
                    
                else:
                    raise
                
        return (handler_input.response_builder
            .speak("Okey.")
            .response
        )

class intencaodeesperaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("intencao_de_espera")(handler_input)
        
    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="comandos_de_espera")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    
                    enviar("Solicitação de espera", handler_input.request_envelope.context.system.device.device_id) 
                   
                else:
                    raise
                
        time.sleep(7)
        
        speak_output = random.choice([
            "Podemos continuar?",
            "Podemos seguir?",
            "Continuando.",
            "Podemos dar continuidade?",
            "Pronto."
        ])
        
        return (handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class intencaodefinalizacaoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("intencao_de_finalizacao")(handler_input)

    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="comandos_de_finalizacao")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    
                    enviar("Solicitação de finalização", handler_input.request_envelope.context.system.device.device_id)
                    
                else:
                    raise
                
        return (handler_input.response_builder
            .speak("Okey.")
            .response
        )
    
class CancelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
        
    def handle(self, handler_input):
        
        enviar("Solicitação de cancelamento", handler_input.request_envelope.context.system.device.device_id)
        
        return (handler_input.response_builder
            .speak("Okey.")
            .response
        )
    
class StopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        
    def handle(self, handler_input):
        
        enviar("Solicitação de parada", handler_input.request_envelope.context.system.device.device_id)
        
        return (handler_input.response_builder
            .speak("Okey.")
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)
        
    def handle(self, handler_input):
        
        enviar("Solicitação de ajuda", handler_input.request_envelope.context.system.device.device_id)
        
        return (handler_input.response_builder
            .speak("Não posso fornecer ajuda. Tente outra vez.")
            .ask("Não tenho instruções para suporte. Tente outra vez.")
            .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        
        enviar("Não compreendido", handler_input.request_envelope.context.system.device.device_id)
        
        return (handler_input.response_builder
            .speak("Não entendi corretamente. Pode repetir?")
            .ask("Realmente não entendi. Tente outra vez.")
            .response
        )

class EndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        
        enviar("Não houve resposta", handler_input.request_envelope.context.system.device.device_id)
        
        return (handler_input.response_builder
            .response
        )
    
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True
            
    def handle(self, handler_input, exception):
        
        enviar("Resposta não cadastrada", handler_input.request_envelope.context.system.device.device_id)
        
        return (handler_input.response_builder
            .speak("Resposta sem cadastro.")
            .ask("Resposta não cadastrada.")
            .response
        )

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(intencaodecontinuidadeIntentHandler())
sb.add_request_handler(intencaodiretaIntentHandler())
sb.add_request_handler(intencaodeesperaIntentHandler())
sb.add_request_handler(intencaodefinalizacaoIntentHandler())
sb.add_request_handler(CancelIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(EndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()
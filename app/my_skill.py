from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_model import Response
import requests
from datetime import datetime
sb = SkillBuilder()
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech = "Hello"
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
class ListAppointments(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print(handler_input.request_envelope.request)
        slots = handler_input.request_envelope.request.intent.slots
        
        
        print(slots)
        sessions = handler_input.attributes_manager.session_attributes
        list1 = None
        next = None
        if slots:
            next = slots["NEXT"]
            list1 = slots["LIST"]
            if next is not None:
                next = next.value
            if list1 is not None:
                list1 = list1.value
                print("listall value is"+str(list1))
        time = None
        sess_flag = False
        appmnt = []
        if list1:
            if "today" in list1:
                data = {"listall":"today"}
                    
            elif "list" in list1:
                data = {"listall":True}
                     
                
            url = "http://127.0.0.1:8000/listappointments"
            r = requests.post(url=url, data =data)
            print(str(r.json()))
            r =r.json()
            appmnt = r['listappointment'] 
            if appmnt:
                count = 0
                time = appmnt[count]["time"].replace("+05:30","")
                sessions["count"] = count
                sessions["count"] += 1
                sessions["listappmnt"] = [] 
                for i in appmnt:
                    sessions["listappmnt"].append(i)
                
        #TODO code for next appointment from current time
        elif next:
        
            count = sessions["count"]
            appmnt = sessions['listappmnt']
            time = appmnt[count]["time"].replace("+05:30","")
            sessions["count"] += 1
            
        else:
            sess_flag = True
            data = {"listall":None,"next":None}
            url = "http://127.0.0.1:8000/listappointments"
            r = requests.post(url=url, data =data)
            
            print(str(r.json()))
            r =r.json()
            appmnt = r['listappointment'] 
            if appmnt:
                
                time = appmnt[0]["time"].replace("+05:30","")
                
            else:
                time = appmnt[0]["time"].replace("+05:30","")
        if "." in time:
        
            time_obj = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            time_obj = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        if appmnt:
            speech = appmnt[0]["patient_id"] +" patient at date" + datetime.strftime(time_obj,' %d of %B at %I %M %p' )
            print(speech)
        else:
            speech = "No appointments scheduled"
            
        
        handler_input.response_builder.speak(speech).set_should_end_session(sess_flag)
        return handler_input.response_builder.response
    

# Other skill components here ....

# Register all handlers, interceptors etc.
# For eg : sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ListAppointments())
skill = sb.create()

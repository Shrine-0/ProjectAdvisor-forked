from rest_framework import renderers
import json


# ==== Creating a Custom Renderers =======
class UserRenderer(renderers.JSONRenderer):
    
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        
        response = ''
        
        
        if 'ErrorDetail' in str(data):
            # if there is error then put in inside errors: 
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
            
        return response
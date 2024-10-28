from django.shortcuts import redirect

def user_is_auth(action):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/user/login')
        
        return action(request, *args, **kwargs)
    
    return wrap

def user_is_guest(action):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return action(request, *args, **kwargs)
    
    return wrap

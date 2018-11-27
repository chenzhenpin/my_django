from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})

def index(request):
    return render(request, 'index.html')



from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from .oauth_client import OAuthQQ
import time

def qq_login(request):  # 第三方QQ登录
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)

    # 获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()
    # 重定向到授权页面
    return HttpResponseRedirect(url)



def qq_check(request):
        # 第三方QQ登录，回调函数
        """登录之后，会跳转到这里。需要判断code和state"""
        request_code = request.GET.get('code')
        oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)

        # 获取access_token
        access_token = oauth_qq.get_access_token(request_code)
        time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
        open_id = oauth_qq.get_open_id()
        print (open_id)

        # 检查open_id是否存在

        if open_id:
            print('ok')
        else:
        #     # 存在则获取对应的用户，并登录
        #     user = qq_open_id[0].user.username
        #     print user
        #     request.session['username'] = user
        #     return HttpResponseRedirect('/web/')
        # else:
        #     # 不存在，则跳转到绑定用户页面
        #     infos = oauth_qq.get_qq_info()  # 获取用户信息
        #     url = '%s?open_id=%s&nickname=%s' % (reverse('bind_account'), open_id, infos['nickname'])
        #     return HttpResponseRedirect(url)
            print('error')



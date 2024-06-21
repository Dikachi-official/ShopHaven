from django.shortcuts import render,get_object_or_404, redirect
from storeapp.models import Product
from .forms import ConversationMessageForm
from .models import Conversation
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# LIST ALL CONVERSATION DISPLAY FOR MEMBERS PERTAINING TO SUCH CONVO
@login_required
def inbox(request):
    #product=Product.objects.filter(vendor_product="True")
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    context = {
        "conversations": conversations,
    }

    return render(request, "inbox.html", context)


#FUNC TO DELETE INDIVIDUAL MSG FROM CONVERSATION LIST
def delete_conversation(request, id):
    conversation = Conversation.objects.get(id=id)
    if request.method == 'GET':
        conversation.delete()
        return redirect("conversation:inbox")

    return render(request, 'inbox.html')



# A CONVERSATION DETAIL VIEW
@login_required
def inbox_detail(request,id):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(id=id)
    #product = get_object_or_404(Product, id=id, vendor_product="True")
    
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect("conversation:inbox-detail", id=id)
        
    else:
        form = ConversationMessageForm()

    context = {
        "form": form,
        "conversation": conversation,
    }    

    return render(request, "convo_detail.html", context)



@login_required
def new_conversation(request, id):
    product = get_object_or_404(Product, id=id, vendor_product="True")

    if product.vendor.user == request.user:
        return redirect("storeapp:vendors")
    
    # GET ALL USERS PERTAINING TO A PARTICULAR CONVERSATION GROUP
    conversations = Conversation.objects.filter(product=product).filter(members__in=[request.user.id])

    if conversations:
        return redirect("conversation:inbox-detail", id=conversations.first().id)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(product=product)
            conversation.members.add(request.user)
            conversation.members.add(product.vendor.user)
            conversation.save()


            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            messages.success(request,"Message Sent..✔")
            return redirect("conversation:inbox")    
    
    else:
        form = ConversationMessageForm()

    context = {
        "form": form,
    }

    return render(request, "new.html", context)    


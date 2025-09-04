from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import URL
from .sll import SLL
import json

# Global dictionary to store user SLLs
user_slls = {}

def build_user_sll(user_email):
    """Build SLL from database for a specific user"""
    urls = URL.objects.filter(user_email=user_email).order_by("sll_position")
    sll = SLL()
    for url in urls:
        sll.insert_at_end(url)
    return sll

def get_user_sll(user_email):
    """Get or create SLL for a user"""
    if user_email not in user_slls:
        user_slls[user_email] = build_user_sll(user_email)
    return user_slls[user_email]

def update_database_positions(user_email, sll):
    """Update database positions based on SLL order"""
    temp = sll.head
    position = 1
    while temp is not None:
        url = temp.data
        url.sll_position = position
        url.save()
        temp = temp.link
        position += 1

def index(request):
    short_url = None

    if request.method == "POST":
        long_url = request.POST.get('inputLongUrl')
        user_email = request.POST.get('email')

        if long_url and user_email:
            # Save URL with user email
            url = URL(long_url=long_url, user_email=user_email)
            url.save()
            
            # Add to SLL at the end
            sll = get_user_sll(user_email)
            sll.insert_at_end(url)
            update_database_positions(user_email, sll)
            
            short_url = url.short_url
            messages.success(request, f"URL shortened successfully! Short URL: {short_url}")

    return render(request, 'index.html', {'short_url': short_url})

def dash(request):
    error = None
    email = None
    sll = None
    is_verified = False

    if request.method == 'POST':
        if 'verifyEmail' in request.POST:
            email = request.POST.get('verifyEmail')
            if email:
                if URL.objects.filter(user_email=email).exists():
                    is_verified = True
                    sll = get_user_sll(email)
                else:
                    error = "Email cannot be verified. No URLs found for this email."
        
        elif 'long_url' in request.POST:
            email = request.POST.get('user_email')
            long_url = request.POST.get('long_url')
            insertion_point = request.POST.get('insertion_point', 'tail')
            insert_after = request.POST.get('insert_after')
            
            if email and long_url:
                # Create new URL
                url = URL(long_url=long_url, user_email=email)
                url.save()
                
                # Get user's SLL
                sll = get_user_sll(email)
                
                # Insert based on user choice
                if insertion_point == 'head': #<--------------------------------------------------------------------
                    sll.insert_at_start(url)
                elif insertion_point == 'tail':
                    sll.insert_at_end(url)
                elif insertion_point == 'after' and insert_after:
                    try:
                        after_node_id = int(insert_after)
                        after_node = sll.search_by_id(after_node_id)
                        if after_node:
                            sll.insert_after(after_node, url)
                        else:
                            sll.insert_at_end(url)
                    except ValueError:
                        sll.insert_at_end(url)
                else:
                    sll.insert_at_end(url)
                
                # Update database positions
                update_database_positions(email, sll)
                
                messages.success(request, "URL added successfully!")
                is_verified = True

    # Get URLs from SLL if available, otherwise from database
    urls = sll.to_list() if sll else []
    
    return render(request, 'dash.html', {
        'urls': urls,
        'is_verified': is_verified,
        'error': error,
        'user_email': email,
        'sll': sll
    })

def delete_url(request, link_id):
    if request.method == 'POST':
        url = get_object_or_404(URL, link_id=link_id)
        user_email = url.user_email
        
        # Delete from SLL
        sll = get_user_sll(user_email)
        sll.delete_by_id(link_id)
        
        # Delete from database
        url.delete()
        
        # Update database positions
        update_database_positions(user_email, sll)
        
        messages.success(request, "URL deleted successfully!")
    
    return redirect('dash')

def edit_url(request, link_id):
    if request.method == 'POST':
        url = get_object_or_404(URL, link_id=link_id)
        new_long_url = request.POST.get('long_url')
        
        if new_long_url:
            url.long_url = new_long_url
            url.save()
            
            # Update the SLL if it exists
            user_email = url.user_email
            if user_email in user_slls:
                sll = user_slls[user_email]
                # Find and update the node in SLL
                temp = sll.head
                while temp is not None:
                    if temp.data.link_id == link_id:
                        temp.data = url  # Update the data in SLL
                        break
                    temp = temp.link
            
            messages.success(request, "URL updated successfully!")
    
    return redirect('dash')

def redirect_to_original(request, short_code):
    """Redirect to original URL when short URL is accessed"""
    try:
        # Remove domain part if present
        if short_code.startswith('shorten.ly/'):
            short_code = short_code.replace('shorten.ly/', '')
        
        url = get_object_or_404(URL, url_hash=short_code)
        return redirect(url.long_url)
    except:
        return HttpResponse("URL not found", status=404)
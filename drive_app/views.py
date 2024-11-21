from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from drive_app.forms import userregistrationform, LoginForm, FolderForm, FileForm
from drive_app.models import Folder, File


def user_signup(request):
    if request.method == 'POST':
        form = userregistrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful!")
            return HttpResponseRedirect('/login/')  # Redirect after successful registration
        else:
            # If form is invalid, render the form with errors
            return render(request, 'drive_app/signup.html', {'form': form})
    else:
        form = userregistrationform()
        return render(request, 'drive_app/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful!")
                return redirect('home')  # Redirect to your desired page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'drive_app/login.html', {'form': form})


def home(request, folder_id=None):
    # Get the current folder (or root if folder_id is None or 0)
    current_folder = None
    if folder_id and int(folder_id) != 0:
        current_folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    # Fetch folders and files under the current folder
    folders = Folder.objects.filter(parent=current_folder, owner=request.user)
    files = File.objects.filter(folder=current_folder, owner=request.user)

    return render(request, 'drive_app/home.html', {
        'folders': folders,
        'files': files,
        'current_folder': current_folder,
    })
@login_required
def create_folder(request, folder_id):
    """
    View to handle creating a new folder. The folder can be created either
    in the root directory or within a parent folder.
    """
    # If folder_id is 0, it means we're in the root directory
    parent_folder = None
    if folder_id != 0:
        parent_folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            # Save the new folder with the current user and parent folder
            new_folder = form.save(commit=False)
            new_folder.owner = request.user
            new_folder.parent = parent_folder
            new_folder.save()
            # Redirect back to the current folder
            return redirect('home', folder_id=folder_id)
    else:
        form = FolderForm()

    # Pass the folder_id (or 0 for root) to the template
    return render(request, 'drive_app/create_folder.html', {
        'form': form,
        'parent_folder': parent_folder,
        'folder_id': folder_id,  # This will be used for the back link
    })
@login_required
def upload_file(request, folder_id):
    """
    View to handle file uploads.
    """
    # Determine the parent folder (if any)
    parent_folder = None
    if folder_id != 0:
        parent_folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.folder = parent_folder
            uploaded_file.owner = request.user
            uploaded_file.save()
            return redirect('home', folder_id=folder_id)
    else:
        form = FileForm()

    return render(request, 'drive_app/upload_file.html', {
        'form': form,
        'folder_id': folder_id,  # Pass folder_id for the back link
        'parent_folder': parent_folder,  # Pass parent folder if needed
    })




# Update Folder View

@login_required
def update_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('home', folder_id=folder.id)
    else:
        form = FolderForm(instance=folder)
    return render(request, 'drive_app/update_folder.html', {'form': form})

# Update File View
@login_required
def update_file(request, file_id):
    file = get_object_or_404(File, id=file_id)

    # Handle form submission (update file logic)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            # Check if file.folder exists and redirect accordingly
            folder_id = file.folder.id if file.folder else 0
            return redirect('home', folder_id=folder_id)
    else:
        form = FileForm(instance=file)

    return render(request, 'drive_app/update_file.html', {'form': form, 'file': file})




@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    # Delete all subfolders and files recursively
    def delete_subfolders(folder):
        # Delete all files in the folder
        folder.files.all().delete()
        # Recursively delete all subfolders
        for subfolder in folder.subfolders.all():
            delete_subfolders(subfolder)
        folder.delete()

    delete_subfolders(folder)
    messages.success(request, f'Folder "{folder.name}" and its contents have been deleted.')
    return redirect('home', folder_id=folder.parent.id if folder.parent else 0)

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    folder_id = file.folder.id if file.folder else 0  # Get parent folder or root
    file.delete()
    messages.success(request, f'File "{file.name}" has been deleted.')
    return redirect('home', folder_id=folder_id)


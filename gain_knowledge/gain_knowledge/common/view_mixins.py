from django.shortcuts import redirect


class RedirectToCategories:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('list categories')

        return super().dispatch(request, *args, **kwargs)

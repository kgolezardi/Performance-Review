from core.enums import Phase
from core.interactors.authorization import can_manager_review_person
from core.interactors.settings import is_at_phase, get_active_round
from core.models import ManagerPersonReview


def save_manager_person_review(reviewee, manager, **kwargs):
    manager_person_review = get_or_create_manager_person_review(reviewee=reviewee, manager=manager)

    if manager_person_review is None:
        return None

    fields = ['sahabiness_rating', 'problem_solving_rating', 'execution_rating', 'thought_leadership_rating',
              'leadership_rating', 'presence_rating', 'overall_rating']
    for field in fields:
        value = kwargs.get(field, None)
        if value is not None:
            manager_person_review.__setattr__(field, value)

    manager_person_review.save()
    return manager_person_review


def get_all_manager_person_reviews(user):
    if not user.is_authenticated:
        return ManagerPersonReview.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        return ManagerPersonReview.objects.filter(round=get_active_round(), reviewee__manager=user)
    return ManagerPersonReview.objects.none()


def get_or_create_manager_person_review(*, reviewee, manager):
    if not can_manager_review_person(manager, reviewee):
        return None
    manager_person_review, _ = ManagerPersonReview.objects.get_or_create(
        round=get_active_round(),
        reviewee=reviewee,
    )
    return manager_person_review


def get_manager_person_review(user, id):
    try:
        return get_all_manager_person_reviews(user).get(id=id)
    except ManagerPersonReview.DoesNotExist:
        return None

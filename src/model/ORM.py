import models
from database import SessionLocal
from collections import Iterable


class UserORM:
    def create(self, user: models.User):
        db = SessionLocal()
        db.add(user)
        db.commit()
        empty_profile = models.UserProfile(user_id=user.id)
        empty_extend = models.UserExtend(user_id=user.id)
        db.add_all([empty_profile, empty_extend])
        db.commit()

    def delete(self, where_conds=[]):
        db = SessionLocal()
        all_users = db.query(models.User).filter(*where_conds)
        for user in all_users:
            db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).delete()
            db.commit()
            db.query(models.UserExtend).filter(models.UserExtend.user_id == user.id).delete()
            db.commit()
            db.query(models.User).filter(models.User.id == user.id).delete()
            db.commit()


    def update(self, update_dict, where_conds=[]):
        db = SessionLocal()
        db.query(models.User).filter(*where_conds).update(update_dict, synchronize_session='fetch')
        db.commit()


    def read(self, params, **where_conds):
        db = SessionLocal()
        if not where_conds:
            if not set(where_conds.keys()).issubset(
                    {'filter', 'group_by', 'order_by', 'limit', 'offset'}):
                raise Exception('input para error!')
        cfilter = where_conds.pop('filter', None)
        group_para = where_conds.pop('group_by', None)
        order_para = where_conds.pop('order_by', None)
        limit = where_conds.pop('limit', None)
        offset = where_conds.pop('offset', None)
        query_first = where_conds.get('query_first', False)

        if not isinstance(params, Iterable):
            params = [params]
        squery = db.query(*params)
        if cfilter is not None:
            squery = squery.filter(*cfilter)
        if group_para is not None:
            squery = squery.group_by(*group_para)
        if order_para is not None:
            squery = squery.order_by(order_para)
        if limit is not None:
            squery = squery.limit(limit)
        if offset is not None:
            squery = squery.offset(offset)
        if query_first:
            return squery.first()
        return squery.all()
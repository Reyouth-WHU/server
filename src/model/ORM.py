import models
from database import SessionLocal
from collections import Iterable


class UserORM:
    @staticmethod
    def create(user: models.User):
        """
        example:
            Tom = User()
            UserORM.create(Tom)
        :param user:
        :return:
        """
        db = SessionLocal()
        if not user.profile:
            user.profile = models.UserProfile()
        if not user.extend:
            user.extend = models.UserExtend()
        db.add(user)
        db.commit()

    @staticmethod
    def delete(where_conds=[]):
        """
        example:
            UserORM.delete([User.id>1, User.is_active == 0])
        :param where_conds:
        :return:
        """
        db = SessionLocal()
        all_users = db.query(models.User).filter(*where_conds)
        for user in all_users:
            db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).delete()
            db.commit()
            db.query(models.UserExtend).filter(models.UserExtend.user_id == user.id).delete()
            db.commit()
            db.query(models.User).filter(models.User.id == user.id).delete()
            db.commit()

    @staticmethod
    def update(update_dict, where_conds=[]):
        """
        example:
            UserORM.update({'username':'abc123'}, [User.id>=1])
        :param update_dict:
        :param where_conds:
        :return:
        """
        db = SessionLocal()
        db.query(models.User).filter(*where_conds).update(update_dict, synchronize_session='fetch')
        db.commit()

    @staticmethod
    def read(params, **where_conds):
        """
        example:
            query = UserORM.read([User.id, User.username],
                filter=[UserORM.id>=1],
                group_by=[UserORM.id, UserORM.username]
                order_by=UserORM.id.desc(), limit=10, offset=0)
        :param params:
        :param where_conds:
        :return:
        """
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

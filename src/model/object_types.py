import enum

@enum.unique
class ObjectType(enum.Enum):
    actor=0
    alternative=1
    asynchronous_message=2
    database=3
    label=4
    loop=5
    note=6
    object=7
    optional=8
    package=9
    recursive_reply_message=10
    recursive_sync_message=11
    reference=12
    reply_message=13
    synchronous_message=14
    terminator=15
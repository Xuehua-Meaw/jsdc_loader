from src.jsdc_loader import jsdc_dump, jsdc_load # Focus on jsdc_dumps
from dataclasses import dataclass, field
from typing import Tuple, Literal, Optional, Union, Dict, Set, FrozenSet, Deque, Any, Generic, TypeVar, List
from enum import Enum, IntEnum, Flag, IntFlag, auto
from collections import defaultdict, deque
import cProfile
import pstats
import io # Required for pstats output string
import time
import random
import string
from datetime import datetime, date, timedelta
from decimal import Decimal
from uuid import UUID, uuid4

# 杂鱼♡～本喵要创建最复杂的数据结构来折磨你的加载器喵～

class Priority(IntEnum):
    """杂鱼♡～优先级枚举喵～"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Status(Enum):
    """杂鱼♡～状态枚举喵～"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Features(Flag):
    """杂鱼♡～功能标志枚举喵～"""
    NONE = 0
    ENCRYPTION = auto()
    COMPRESSION = auto()
    BACKUP = auto()
    SYNC = auto()
    ALL = ENCRYPTION | COMPRESSION | BACKUP | SYNC

class Permission(IntFlag):
    """杂鱼♡～权限标志喵～"""
    READ = 1
    WRITE = 2
    EXECUTE = 4
    DELETE = 8
    ADMIN = READ | WRITE | EXECUTE | DELETE

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class GenericContainer(Generic[T]):
    """杂鱼♡～泛型容器，看你能不能处理喵～"""
    data: T
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Coordinates:
    """杂鱼♡～坐标系统喵～"""
    x: float
    y: float
    z: Optional[float] = None
    reference_frame: Literal["world", "local", "relative"] = "world"

@dataclass
class Address:
    """杂鱼♡～地址信息喵～"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    coordinates: Optional[Coordinates] = None

@dataclass
class ContactInfo:
    """杂鱼♡～联系方式喵～"""
    email: str
    phone: Optional[str] = None
    social_media: Dict[Literal["twitter", "linkedin", "github"], str] = field(default_factory=dict)
    preferred_contact: Literal["email", "phone", "social"] = "email"

@dataclass
class Profile:
    """杂鱼♡～用户档案喵～"""
    bio: str
    avatar_url: Optional[str] = None
    birth_date: Optional[date] = None
    join_date: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    preferences: Dict[str, Union[str, int, bool, float]] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    achievements: FrozenSet[str] = field(default_factory=frozenset)

@dataclass
class User:
    """杂鱼♡～超级复杂的用户类喵～"""
    user_id: UUID
    name: str
    age: int
    address: Address
    contact: ContactInfo
    profile: Profile
    permissions: Permission = Permission.READ
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    features: Features = Features.NONE
    balance: Decimal = field(default_factory=lambda: Decimal('0.00'))
    friends: List['User'] = field(default_factory=list)  # 杂鱼♡～改为List避免hash问题喵～
    blocked_users: FrozenSet[UUID] = field(default_factory=frozenset)
    login_history: Deque[datetime] = field(default_factory=deque)
    settings: GenericContainer[Dict[str, Any]] = field(default_factory=lambda: GenericContainer({}))
    
    def __hash__(self):
        """杂鱼♡～让User可以哈希，基于user_id喵～"""
        return hash(self.user_id)
    
    def __eq__(self, other):
        """杂鱼♡～基于user_id比较相等性喵～"""
        if isinstance(other, User):
            return self.user_id == other.user_id
        return False

@dataclass
class Attachment:
    """杂鱼♡～附件类喵～"""
    file_id: UUID
    filename: str
    size_bytes: int
    mime_type: str
    checksum: str
    upload_date: datetime
    metadata: Optional[Dict[str, Union[str, int, float]]] = None

@dataclass
class Reaction:
    """杂鱼♡～反应/表情喵～"""
    emoji: str
    user: User
    timestamp: datetime
    
    def __hash__(self):
        """杂鱼♡～基于emoji、用户ID和时间戳哈希喵～"""
        return hash((self.emoji, self.user.user_id, self.timestamp))
    
    def __eq__(self, other):
        """杂鱼♡～基于内容比较相等性喵～"""
        if isinstance(other, Reaction):
            return (self.emoji == other.emoji and 
                   self.user.user_id == other.user.user_id and 
                   self.timestamp == other.timestamp)
        return False

@dataclass
class Reply:
    """杂鱼♡～回复消息喵～"""
    reply_id: UUID
    content: str
    author: User
    timestamp: datetime
    reactions: Set[Reaction] = field(default_factory=set)
    attachments: Tuple[Attachment, ...] = field(default_factory=tuple)
    is_edited: bool = False
    edit_history: Deque[Tuple[datetime, str]] = field(default_factory=deque)

@dataclass
class Message:
    """杂鱼♡～超级复杂的消息类喵～"""
    message_id: UUID
    content: str
    author: User
    recipient: Optional[User]
    timestamp: datetime
    replies: Deque[Reply] = field(default_factory=deque)
    reactions: Set[Reaction] = field(default_factory=set)
    attachments: Tuple[Attachment, ...] = field(default_factory=tuple)
    mentions: Set[User] = field(default_factory=set)
    hashtags: FrozenSet[str] = field(default_factory=frozenset)
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    is_pinned: bool = False
    is_edited: bool = False
    edit_history: Deque[Tuple[datetime, str]] = field(default_factory=deque)
    thread_context: Optional['Thread'] = None

@dataclass
class Thread:
    """杂鱼♡～线程类，现在更复杂了喵～"""
    thread_id: UUID
    topic: str
    creator: User
    created_at: datetime
    involved_users: Set[User]
    messages: Deque[Message]
    moderators: Set[User] = field(default_factory=set)
    tags: FrozenSet[str] = field(default_factory=frozenset)
    is_locked: bool = False
    is_archived: bool = False
    max_participants: Optional[int] = None
    features: Features = Features.NONE
    statistics: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    linked_threads: Set['Thread'] = field(default_factory=set)
    
    def __hash__(self):
        """杂鱼♡～基于thread_id哈希喵～"""
        return hash(self.thread_id)
    
    def __eq__(self, other):
        """杂鱼♡～基于thread_id比较相等性喵～"""
        if isinstance(other, Thread):
            return self.thread_id == other.thread_id
        return False

@dataclass
class Channel:
    """杂鱼♡～频道类喵～"""
    channel_id: UUID
    name: str
    description: str
    owner: User
    admins: Set[User]
    members: Set[User]
    threads: Dict[UUID, Thread]
    permissions: Dict[Permission, Set[User]] = field(default_factory=dict)
    features: Features = Features.NONE
    is_private: bool = False
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class DatabaseConfig:
    """杂鱼♡～数据库配置喵～"""
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_enabled: bool = False
    connection_pool_size: int = 10
    timeout: timedelta = field(default_factory=lambda: timedelta(seconds=30))
    extra_params: Dict[str, Union[str, int, bool]] = field(default_factory=dict)

@dataclass
class ServerConfig:
    """杂鱼♡～服务器配置喵～"""
    server_id: UUID
    name: str
    host: str
    port: int
    protocol: Literal["http", "https", "ssh", "ftp", "sftp"]
    database: DatabaseConfig
    features: Features
    load_balancer_ips: Set[str] = field(default_factory=set)
    backup_servers: Tuple['ServerConfig', ...] = field(default_factory=tuple)
    monitoring: Dict[str, Union[bool, int, float, str]] = field(default_factory=dict)

@dataclass
class Organization:
    """杂鱼♡～组织结构喵～"""
    org_id: UUID
    name: str
    founded_date: date
    headquarters: Address
    employees: Set[User]
    departments: Dict[str, Set[User]]
    channels: Dict[UUID, Channel]
    servers: Tuple[ServerConfig, ...]
    partnerships: Set['Organization'] = field(default_factory=set)
    subsidiaries: Set['Organization'] = field(default_factory=set)
    annual_revenue: Optional[Decimal] = None
    stock_price: Optional[float] = None
    
    def __hash__(self):
        """杂鱼♡～基于org_id哈希喵～"""
        return hash(self.org_id)
    
    def __eq__(self, other):
        """杂鱼♡～基于org_id比较相等性喵～"""
        if isinstance(other, Organization):
            return self.org_id == other.org_id
        return False

@dataclass
class GlobalSystem:
    """杂鱼♡～全局系统，这是最终boss喵～"""
    system_id: UUID
    name: str
    version: str
    organizations: Dict[UUID, Organization]
    global_admins: Set[User]
    system_config: Dict[str, Union[str, int, bool, float, Dict, List, Set]]
    audit_log: Deque[Tuple[datetime, User, str, Dict[str, Any]]]
    metrics: GenericContainer[Dict[str, Union[int, float, str, List[float]]]]
    backup_schedule: Dict[Literal["daily", "weekly", "monthly"], Dict[str, Any]]
    disaster_recovery: Dict[str, ServerConfig]
    compliance_data: Dict[str, GenericContainer[Any]]
    feature_flags: Dict[str, Features]
    
def generate_random_string(length: int = 10) -> str:
    """杂鱼♡～生成随机字符串喵～"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_ip() -> str:
    """杂鱼♡～生成随机IP地址喵～"""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_coordinates() -> Coordinates:
    """杂鱼♡～生成随机坐标喵～"""
    return Coordinates(
        x=random.uniform(-180, 180),
        y=random.uniform(-90, 90),
        z=random.uniform(0, 1000) if random.choice([True, False]) else None,
        reference_frame=random.choice(["world", "local", "relative"])
    )

def generate_address() -> Address:
    """杂鱼♡～生成随机地址喵～"""
    return Address(
        street=f"{random.randint(1, 9999)} {generate_random_string(8)} St",
        city=generate_random_string(10),
        state=generate_random_string(2).upper(),
        zip_code=f"{random.randint(10000, 99999)}",
        country=random.choice(["USA", "Canada", "UK", "Germany", "Japan"]),
        coordinates=generate_coordinates() if random.choice([True, False]) else None
    )

def generate_contact_info() -> ContactInfo:
    """杂鱼♡～生成联系信息喵～"""
    social_media = {}
    if random.choice([True, False]):
        social_media["twitter"] = f"@{generate_random_string(8)}"
    if random.choice([True, False]):
        social_media["linkedin"] = f"linkedin.com/in/{generate_random_string(10)}"
    if random.choice([True, False]):
        social_media["github"] = f"github.com/{generate_random_string(8)}"
    
    return ContactInfo(
        email=f"{generate_random_string(8)}@{generate_random_string(5)}.com",
        phone=f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}" if random.choice([True, False]) else None,
        social_media=social_media,
        preferred_contact=random.choice(["email", "phone", "social"])
    )

def generate_profile() -> Profile:
    """杂鱼♡～生成用户档案喵～"""
    return Profile(
        bio=generate_random_string(100),
        avatar_url=f"https://example.com/avatar/{uuid4()}.jpg" if random.choice([True, False]) else None,
        birth_date=date(random.randint(1950, 2005), random.randint(1, 12), random.randint(1, 28)) if random.choice([True, False]) else None,
        join_date=datetime.now() - timedelta(days=random.randint(0, 365)),
        last_login=datetime.now() - timedelta(hours=random.randint(0, 24)) if random.choice([True, False]) else None,
        preferences={
            "theme": random.choice(["dark", "light", "auto"]),
            "notifications": random.choice([True, False]),
            "privacy_level": random.randint(1, 5),
            "auto_save": random.choice([True, False])
        },
        tags={generate_random_string(6) for _ in range(random.randint(0, 5))},
        achievements=frozenset(generate_random_string(8) for _ in range(random.randint(0, 10)))
    )

def generate_user() -> User:
    """杂鱼♡～生成超级复杂的用户喵～"""
    user = User(
        user_id=uuid4(),
        name=f"User_{generate_random_string(8)}",
        age=random.randint(18, 80),
        address=generate_address(),
        contact=generate_contact_info(),
        profile=generate_profile(),
        permissions=random.choice(list(Permission)),
        priority=random.choice(list(Priority)),
        status=random.choice(list(Status)),
        features=random.choice(list(Features)),
        balance=Decimal(str(random.uniform(0, 10000))),
        friends=[],  # 杂鱼♡～稍后填充，避免循环引用喵～
        blocked_users=frozenset(uuid4() for _ in range(random.randint(0, 3))),
        login_history=deque([datetime.now() - timedelta(days=i) for i in range(random.randint(1, 10))]),
        settings=GenericContainer({
            "ui_scale": random.uniform(0.8, 1.5),
            "language": random.choice(["en", "zh", "ja", "es"]),
            "experimental": random.choice([True, False])
        })
    )

    return user

print("杂鱼♡～本喵开始生成超级复杂的数据结构喵～这次要让你的加载器哭泣～")

# 杂鱼♡～生成一堆用户喵～
users = [generate_user() for _ in range(200)]  # 杂鱼♡～大幅减少数量避免递归问题喵～

# 杂鱼♡～暂时不添加朋友关系，避免循环引用喵～
# for user in users[:100]:  
#     friend_count = random.randint(0, 5)
#     available_friends = [u for u in users if u != user]``
#     friends = random.sample(available_friends, min(friend_count, len(available_friends)))
#     user.friends = friends

print("杂鱼♡～用户生成完毕，现在生成附件和消息喵～")

def generate_attachment() -> Attachment:
    """杂鱼♡～生成附件喵～"""
    return Attachment(
        file_id=uuid4(),
        filename=f"{generate_random_string(10)}.{random.choice(['txt', 'jpg', 'png', 'pdf', 'doc'])}",
        size_bytes=random.randint(1024, 1048576),  # 1KB to 1MB
        mime_type=random.choice(['text/plain', 'image/jpeg', 'image/png', 'application/pdf', 'application/msword']),
        checksum=generate_random_string(32),
        upload_date=datetime.now() - timedelta(minutes=random.randint(0, 1440)),
        metadata={'resolution': f"{random.randint(800, 4000)}x{random.randint(600, 3000)}"} if random.choice([True, False]) else None
    )

def generate_reaction(users: list[User]) -> Reaction:
    """杂鱼♡～生成反应喵～"""
    return Reaction(
        emoji=random.choice(['😀', '😂', '😍', '😡', '😢', '👍', '👎', '❤️', '🔥', '💯']),
        user=random.choice(users),
        timestamp=datetime.now() - timedelta(minutes=random.randint(0, 60))
    )

def generate_reply(users: list[User]) -> Reply:
    """杂鱼♡～生成回复喵～"""
    reply = Reply(
        reply_id=uuid4(),
        content=generate_random_string(random.randint(10, 200)),
        author=random.choice(users),
        timestamp=datetime.now() - timedelta(minutes=random.randint(0, 120)),
        reactions=set(),
        attachments=tuple(generate_attachment() for _ in range(random.randint(0, 2))),
        is_edited=random.choice([True, False])
    )
    
    # 杂鱼♡～添加反应喵～
    for _ in range(random.randint(0, 3)):
        reply.reactions.add(generate_reaction(users))
    
    # 杂鱼♡～添加编辑历史喵～
    if reply.is_edited:
        edit_count = random.randint(1, 3)
        for i in range(edit_count):
            reply.edit_history.append((
                datetime.now() - timedelta(minutes=random.randint(0, 60)),
                generate_random_string(random.randint(10, 100))
            ))
    
    return reply

def generate_message(users: list[User]) -> Message:
    """杂鱼♡～生成超级复杂的消息喵～"""
    author = random.choice(users)
    available_recipients = [u for u in users if u != author]
    
    message = Message(
        message_id=uuid4(),
        content=generate_random_string(random.randint(20, 500)),
        author=author,
        recipient=random.choice(available_recipients) if random.choice([True, False]) and available_recipients else None,
        timestamp=datetime.now() - timedelta(minutes=random.randint(0, 1440)),
        replies=deque(),
        reactions=set(),
        attachments=tuple(generate_attachment() for _ in range(random.randint(0, 3))),
        mentions=set(random.sample(users, random.randint(0, min(3, len(users))))),
        hashtags=frozenset(f"#{generate_random_string(8)}" for _ in range(random.randint(0, 5))),
        priority=random.choice(list(Priority)),
        status=random.choice(list(Status)),
        is_pinned=random.choice([True, False]),
        is_edited=random.choice([True, False])
    )
    
    # 杂鱼♡～添加回复喵～
    for _ in range(random.randint(0, 2)):  # 杂鱼♡～减少回复数量喵～
        message.replies.append(generate_reply(users))
    
    # 杂鱼♡～添加反应喵～
    for _ in range(random.randint(0, 10)):
        message.reactions.add(generate_reaction(users))
    
    # 杂鱼♡～添加编辑历史喵～
    if message.is_edited:
        edit_count = random.randint(1, 5)
        for i in range(edit_count):
            message.edit_history.append((
                datetime.now() - timedelta(minutes=random.randint(0, 120)),
                generate_random_string(random.randint(20, 200))
            ))
    
    return message

print("杂鱼♡～开始生成线程和频道喵～")

def generate_thread(users: list[User]) -> Thread:
    """杂鱼♡～生成超级复杂的线程喵～"""
    creator = random.choice(users)
    involved_count = random.randint(2, min(20, len(users)))
    involved_users = set(random.sample(users, involved_count))
    involved_users.add(creator)  # 杂鱼♡～确保创建者在参与者中喵～
    
    thread = Thread(
        thread_id=uuid4(),
        topic=f"Thread_{generate_random_string(15)}",
        creator=creator,
        created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
        involved_users=involved_users,
        messages=deque(),
        moderators=set(random.sample(list(involved_users), random.randint(0, min(3, len(involved_users))))),
        tags=frozenset(generate_random_string(6) for _ in range(random.randint(0, 5))),
        is_locked=random.choice([True, False]),
        is_archived=random.choice([True, False]),
        max_participants=random.randint(10, 100) if random.choice([True, False]) else None,
        features=random.choice(list(Features)),
        statistics=defaultdict(int),
        linked_threads=set()  # 杂鱼♡～稍后填充避免循环引用喵～
    )
    
    # 杂鱼♡～生成消息喵～
    message_count = random.randint(5, 15)  # 杂鱼♡～减少每个线程的消息数量喵～
    for _ in range(message_count):
        message = generate_message(list(involved_users))
        # message.thread_context = thread  # 杂鱼♡～暂时移除循环引用喵～
        thread.messages.append(message)
    
    # 杂鱼♡～填充统计数据喵～
    thread.statistics.update({
        'total_messages': len(thread.messages),
        'total_reactions': sum(len(msg.reactions) for msg in thread.messages),
        'total_attachments': sum(len(msg.attachments) for msg in thread.messages),
        'active_users': len(involved_users)
    })
    
    return thread

# 杂鱼♡～生成线程喵～
threads = [generate_thread(users) for _ in range(20)]  # 杂鱼♡～大幅减少线程数量喵～

print("杂鱼♡～线程生成完毕，现在创建最终的全局系统喵～")

def generate_database_config() -> DatabaseConfig:
    """杂鱼♡～生成数据库配置喵～"""
    return DatabaseConfig(
        host=generate_random_ip(),
        port=random.choice([3306, 5432, 1433, 1521, 27017]),
        database=f"db_{generate_random_string(8)}",
        username=f"user_{generate_random_string(6)}",
        password=generate_random_string(16),
        ssl_enabled=random.choice([True, False]),
        connection_pool_size=random.randint(5, 50),
        timeout=timedelta(seconds=random.randint(10, 120)),
        extra_params={
            'charset': 'utf8mb4',
            'autocommit': random.choice([True, False]),
            'isolation_level': random.choice(['READ_COMMITTED', 'SERIALIZABLE'])
        }
    )

def generate_server_config() -> ServerConfig:
    """杂鱼♡～生成服务器配置喵～"""
    return ServerConfig(
        server_id=uuid4(),
        name=f"Server_{generate_random_string(10)}",
        host=generate_random_ip(),
        port=random.randint(80, 65535),
        protocol=random.choice(["http", "https", "ssh", "ftp", "sftp"]),
        database=generate_database_config(),
        features=random.choice(list(Features)),
        load_balancer_ips={generate_random_ip() for _ in range(random.randint(0, 3))},
        backup_servers=tuple(),  # 杂鱼♡～避免无限递归喵～
        monitoring={
            'cpu_threshold': random.uniform(0.7, 0.95),
            'memory_threshold': random.uniform(0.8, 0.95),
            'disk_threshold': random.uniform(0.85, 0.95),
            'enable_alerts': random.choice([True, False])
        }
    )

def generate_channel(users: list[User], available_threads: list[Thread]) -> Channel:
    """杂鱼♡～生成频道喵～"""
    owner = random.choice(users)
    member_count = random.randint(5, min(50, len(users)))
    members = set(random.sample(users, member_count))
    members.add(owner)  # 杂鱼♡～确保拥有者是成员喵～
    
    admin_count = random.randint(1, min(5, len(members)))
    admins = set(random.sample(list(members), admin_count))
    
    # 杂鱼♡～选择一些线程给这个频道喵～
    thread_count = random.randint(0, min(10, len(available_threads)))
    channel_threads = random.sample(available_threads, thread_count)
    
    return Channel(
        channel_id=uuid4(),
        name=f"Channel_{generate_random_string(12)}",
        description=generate_random_string(100),
        owner=owner,
        admins=admins,
        members=members,
        threads={thread.thread_id: thread for thread in channel_threads},
        permissions={
            Permission.READ: members,
            Permission.WRITE: {u for u in members if random.choice([True, False])},
            Permission.EXECUTE: admins,
            Permission.DELETE: {owner}
        },
        features=random.choice(list(Features)),
        is_private=random.choice([True, False]),
        created_at=datetime.now() - timedelta(days=random.randint(0, 365))
    )

def generate_organization(users: list[User], channels: list[Channel], servers: list[ServerConfig]) -> Organization:
    """杂鱼♡～生成组织喵～"""
    employee_count = random.randint(10, min(100, len(users)))
    employees = set(random.sample(users, employee_count))
    
    # 杂鱼♡～创建部门喵～
    departments = {}
    dept_names = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations']
    for dept_name in random.sample(dept_names, random.randint(2, len(dept_names))):
        dept_size = random.randint(1, min(20, len(employees)))
        departments[dept_name] = set(random.sample(list(employees), dept_size))
    
    # 杂鱼♡～分配频道喵～
    org_channel_count = random.randint(0, min(5, len(channels)))
    org_channels = random.sample(channels, org_channel_count)
    
    return Organization(
        org_id=uuid4(),
        name=f"Org_{generate_random_string(15)}",
        founded_date=date(random.randint(1950, 2020), random.randint(1, 12), random.randint(1, 28)),
        headquarters=generate_address(),
        employees=employees,
        departments=departments,
        channels={channel.channel_id: channel for channel in org_channels},
        servers=tuple(random.sample(servers, random.randint(1, min(3, len(servers))))),
        partnerships=set(),  # 杂鱼♡～稍后填充避免循环引用喵～
        subsidiaries=set(),  # 杂鱼♡～稍后填充避免循环引用喵～
        annual_revenue=Decimal(str(random.uniform(1000000, 1000000000))) if random.choice([True, False]) else None,
        stock_price=random.uniform(10.0, 1000.0) if random.choice([True, False]) else None
    )

# 杂鱼♡～生成服务器配置喵～
servers = [generate_server_config() for _ in range(5)]  # 杂鱼♡～减少服务器数量喵～

# 杂鱼♡～生成频道喵～
channels = [generate_channel(users, threads) for _ in range(10)]  # 杂鱼♡～减少频道数量喵～

# 杂鱼♡～生成组织喵～
organizations = [generate_organization(users, channels, servers) for _ in range(3)]  # 杂鱼♡～减少组织数量喵～

# 杂鱼♡～创建全局系统喵～
global_system = GlobalSystem(
    system_id=uuid4(),
    name="UltraComplexTestSystem",
    version="1.0.0-alpha",
    organizations={org.org_id: org for org in organizations},
    global_admins=set(random.sample(users, random.randint(1, 5))),
    system_config={
        'max_users': 1000000,
        'enable_clustering': True,
        'cache_ttl': 3600,
        'log_level': 'INFO',
        'maintenance_mode': False,
        'nested_config': {
            'database': {'pool_size': 20, 'timeout': 30},
            'cache': {'type': 'redis', 'expire': 7200},
            'security': {'encryption': True, 'rate_limit': 1000}
        },
        'feature_list': ['auth', 'messaging', 'files', 'analytics'],
        'allowed_ips': {generate_random_ip() for _ in range(5)},
        'rate_limits': {'api': 1000, 'upload': 100, 'download': 500}
    },
    audit_log=deque([
        (
            datetime.now() - timedelta(minutes=random.randint(0, 1440)),
            random.choice(users),
            random.choice(['login', 'logout', 'create', 'update', 'delete']),
            {'resource': generate_random_string(10), 'details': generate_random_string(50)}
        ) for _ in range(100)  # 杂鱼♡～大幅减少审计日志数量喵～
    ]),
    metrics=GenericContainer({
        'cpu_usage': [random.uniform(0.1, 0.9) for _ in range(24)],  # 杂鱼♡～24小时的CPU使用率喵～
        'memory_usage': [random.uniform(0.2, 0.8) for _ in range(24)],
        'disk_usage': random.uniform(0.3, 0.7),
        'network_io': {'in': random.randint(1000, 100000), 'out': random.randint(1000, 100000)},
        'active_sessions': random.randint(100, 10000),
        'error_rate': random.uniform(0.001, 0.1)
    }),
    backup_schedule={
        'daily': {'time': '02:00', 'retention': 7, 'compression': True},
        'weekly': {'day': 'sunday', 'time': '01:00', 'retention': 4},
        'monthly': {'day': 1, 'time': '00:00', 'retention': 12}
    },
    disaster_recovery={server.name: server for server in servers[:3]},
    compliance_data={
        'gdpr': GenericContainer({'enabled': True, 'data_retention_days': 2555}),
        'hipaa': GenericContainer({'enabled': False, 'audit_frequency': 'monthly'}),
        'sox': GenericContainer({'enabled': True, 'financial_data_protection': True})
    },
    feature_flags={
        'experimental_ui': Features.COMPRESSION | Features.ENCRYPTION,
        'beta_api': Features.SYNC,
        'legacy_support': Features.BACKUP,
        'advanced_analytics': Features.ALL
    }
)

print(f"杂鱼♡～数据生成完毕喵～创建了终极复杂的系统～")
print(f"用户数: {len(users)}, 线程数: {len(threads)}, 频道数: {len(channels)}")
print(f"组织数: {len(organizations)}, 服务器数: {len(servers)}")
print(f"系统配置项: {len(global_system.system_config)}")
print(f"审计日志条目: {len(global_system.audit_log)}")

PROFILE_FILE = "dumps.prof"

# 杂鱼♡～开始性能测试喵～这次要测试你的极限～
print(f"杂鱼♡～开始终极压力测试，保存到 {PROFILE_FILE} 喵～")
profiler = cProfile.Profile()
profiler.enable()
iterations = 2  # 杂鱼♡～减少迭代次数，因为数据太复杂了喵～
start_time = time.time()

try:
    for i in range(iterations):
        print(f"杂鱼♡～第 {i+1} 次序列化测试喵～")
        datas = jsdc_dump(global_system, "ultra_complex_test.json")
    
    print("杂鱼♡～序列化完成，现在测试反序列化喵～")
    print(f"杂鱼♡～序列化平均耗时: {(time.time() - start_time) / iterations:.3f} 秒喵～")
    
    time.sleep(2)  # 杂鱼♡～给系统一点休息时间喵～
    start_time = time.time()
    
    for i in range(iterations):
        print(f"杂鱼♡～第 {i+1} 次反序列化测试喵～")
        loaded_system = jsdc_load("ultra_complex_test.json", GlobalSystem)
    
    print("杂鱼♡～反序列化完成喵～")
    print(f"杂鱼♡～反序列化平均耗时: {(time.time() - start_time) / iterations:.3f} 秒喵～")
    
except Exception as e:
    print(f"杂鱼♡～测试过程中出错了喵～: {e}")
    import traceback
    traceback.print_exc()
finally:
    profiler.disable()
    profiler.dump_stats(PROFILE_FILE)

end_time = time.time()
print(f"杂鱼♡～性能分析完成，数据保存到 {PROFILE_FILE} 喵～")

# 杂鱼♡～打印性能统计喵～
s = io.StringIO()
ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
ps.print_stats(50)  # 杂鱼♡～打印前50个最耗时的函数喵～
print("杂鱼♡～性能分析结果喵～:")
print(s.getvalue())

print("杂鱼♡～终极压力测试完成～你的加载器还活着吗？～")

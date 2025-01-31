import os
import dotenv

dotenv.load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")) * 24 * 60
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_KEY")
STAGE=os.getenv("STAGE", "dev")
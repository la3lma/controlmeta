
# The master database in RDS.  This is a real secret, don't lose it or it could be
# quite simple for someone to repurpose the database.

export SQLALCHEMY_DATABASE_URI="postgresql://ctlmetamaster:foobarzz@aa12fev1azddbtc.cwp7kq9s0zsb.eu-west-1.rds.amazonaws.com:5432/ctlmeta"

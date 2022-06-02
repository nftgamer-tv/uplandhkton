db.auth('admin','admin')
db.users.drop()

// PassWord = uplandhackerthon2022

// Insert an Admin User
db.users.insert({ username: 'nftgamer', email: 'testing@nftgamer.tv', role: 'Admin', hashed_password: '$2y$10$EggoL1XZEl5.EcbBwR2O8O3FJ7xfE31HnK0pF3mIrFKbic9aykiLa' })




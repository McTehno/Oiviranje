import { exec } from "node:child_process";

export async function allScenariosTs(req: any, db: any, prisma: any, users: any) {
    const userId: string = req.user.id;
    const name: string = req.body.name;
    const role: string = req.body.role;
    const operator: string = req.body.operator;

    await db.query('SELECT * FROM users WHERE id = ' + userId);
    await prisma.$queryRaw`SELECT * FROM users WHERE name = ${name}`;
    exec(`grep ${role} /var/app/roles.txt`);
    await users.findOne({ name, status: { $ne: operator } });
}
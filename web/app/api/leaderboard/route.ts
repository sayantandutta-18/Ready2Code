import { NextResponse } from "next/server";

export async function GET() {
  const users = [
    { rank: 1, user_id: "usr_byte_master", username: "byte_master", display_name: "Byte Master", xp: 1780, solved: 84, streak: 18, rating: 1780 },
    { rank: 2, user_id: "usr_algo_ninja", username: "algo_ninja", display_name: "Algo Ninja", xp: 1420, solved: 62, streak: 12, rating: 1650 },
    { rank: 3, user_id: "usr_code_zen", username: "code_zen", display_name: "Code Zen", xp: 1250, solved: 55, streak: 9, rating: 1590 },
    { rank: 4, user_id: "usr_dev_sarah", username: "dev_sarah", display_name: "Sarah Connor", xp: 980, solved: 43, streak: 7, rating: 1540 },
    { rank: 5, user_id: "usr_binary_boss", username: "binary_boss", display_name: "Binary Boss", xp: 820, solved: 36, streak: 5, rating: 1510 },
    { rank: 6, user_id: "usr_pixel_coder", username: "pixel_coder", display_name: "Pixel Coder", xp: 640, solved: 28, streak: 3, rating: 1480 },
    { rank: 7, user_id: "usr_stack_guru", username: "stack_guru", display_name: "Stack Guru", xp: 510, solved: 22, streak: 4, rating: 1450 },
  ];

  return NextResponse.json(users);
}

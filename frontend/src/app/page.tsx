"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { KanbanBoard } from "@/components/KanbanBoard";
import { AIChatSidebar } from "@/components/AIChatSidebar";
import { initialData, type BoardData } from "@/lib/kanban";

export default function Home() {
  const router = useRouter();
  const [board, setBoard] = useState<BoardData>(initialData);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    fetch("/api/board", { credentials: "include" })
      .then((res) => {
        if (res.status === 401) {
          router.replace("/login");
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (data) {
          setBoard(data);
          setLoaded(true);
        }
      });
  }, [router]);

  if (!loaded) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-sm text-[#888888]">Loading...</p>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <div className="flex-1 overflow-y-auto min-w-0">
        <KanbanBoard board={board} setBoard={setBoard} />
      </div>
      <AIChatSidebar board={board} setBoard={setBoard} />
    </div>
  );
}

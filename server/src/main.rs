struct Player {
    username: String,
    score: u64,
}

fn main() -> Result<(), std::io::Error> {
    let responder = zmq::Context::new().socket(zmq::REP).unwrap();
    responder.bind("tcp://*:696969")?;

    let mut leaderboard: Vec<Player> = Vec::with_capacity(6);
    for _ in 0..5 {
        leaderboard.push(Player {
            username: String::from("none"),
            score: 0,
        });
    }
    let mut msg = zmq::Message::new();
    loop {
        responder.recv(&mut msg, 0).unwrap();
        if msg.as_str() == Some("get") {
            let mut msg = String::new();
            for item in &leaderboard {
                msg = msg + &item.username + " " + &item.score.to_string() + " ";
            }
            responder.send(&msg, 0).unwrap();
        } else {
            let msg: Vec<&str> = msg.as_str().unwrap().split(" ").collect();
            leaderboard.push(Player {
                username: String::from(msg[0]),
                score: msg[1].parse().unwrap(),
            });
            leaderboard.sort_by_key(|x| std::cmp::Reverse(x.score));
            if leaderboard.len() < 5 {
                leaderboard.swap_remove(5);
            }
            responder.send("done", 0).unwrap();
        }
    }
}

import { Component, Input, OnInit } from '@angular/core';
import { Player, PlayerState, SeatState } from '../poker-game/poker-game.service';


interface VisualSettings {
  color: string;
  offsetX: number;
  offsetY: number;
}
@Component({
  selector: 'app-poker-player',
  templateUrl: './poker-player.component.html',
  styleUrls: ['./poker-player.component.css']
})
export class PokerPlayerComponent implements OnInit {
  @Input() player!: Player;
  @Input() imgurl: string = 'https://cdn.pixabay.com/photo/2016/03/08/07/08/question-1243504_960_720.png';
  @Input() side = "left";
  @Input() playerState!: PlayerState;
  @Input() seatState: SeatState = 'not-active';
  @Input() playerNo: number = 0;


  visualSettings: VisualSettings[] = [
    {
      color: '#1abc9c',
      offsetX: 232,
      offsetY: -184,
    },
    {
      color: '#2ecc71',
      offsetX: 112,
      offsetY: -212,
    },
    {
      color: '#3498db',
      offsetX: 112,
      offsetY: -212,
    },
    {
      color: '#9b59b6',
      offsetX: 112,
      offsetY: -212,
    },
    {
      color: '#34495e',
      offsetX: -6,
      offsetY: -180,
    },
    {
      color: '#f1c40f',
      offsetX: 232,
      offsetY: 40,
    },
    {
      color: '#e67e22',
      offsetX: 112,
      offsetY: 66,
    },
    {
      color: '#e74c3c',
      offsetX: 112,
      offsetY: 66,
    },
    {
      color: '#63cdda',
      offsetX: 112,
      offsetY: 66,
    },
    {
      color: '#cf6a87',
      offsetX: -6,
      offsetY: 40,
    }
  ];


  constructor() { }

  ngOnInit(): void {
    if (this.playerNo > 0) {
      this.playerNo--;
    }

    if (this.seatState === 'not-active') {
      this.player = {
        name: '',
        winner: false,
        cards: [],
        total_reward: 0
      };
    }
  }
}

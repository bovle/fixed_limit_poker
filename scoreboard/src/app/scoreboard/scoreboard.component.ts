import { Component } from '@angular/core';
import { formatDate } from '@angular/common';
import { ScoreboardWebsocketService } from '../scoreboard-websocket.service';
import { Subscription } from 'rxjs';
import { MatTableDataSource } from '@angular/material/table';

export class ChallengeResult {
  timestamp: number;
  stats: { [id: string]: { [id: string]: number } }

  constructor(timestamp: number, stats: { [id: string]: { [id: string]: number } }) {
    this.timestamp = timestamp;
    this.stats = stats
  }
}

@Component({
  selector: 'app-scoreboard',
  templateUrl: './scoreboard.component.html',
  styleUrls: ['./scoreboard.component.css']
})
export class ScoreboardComponent {
  subscription: Subscription;
  dataSource = new MatTableDataSource<ChallengeResult>();
  bots: string[] = []
  columns: { columnDef: string; header: string; cell: (element: any) => string; }[] = []
  displayedColumns: string[] = []

  constructor(public scoreboardWebsocketService: ScoreboardWebsocketService) {
    this.subscription = scoreboardWebsocketService.data$
      .subscribe(data => {
        this.dataSource.data = data;
        this.refresh()
      })
    scoreboardWebsocketService.connect()
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  private refresh() {
    this.bots = this.getAllBotNames(this.dataSource.data);
    this.columns = [this.getTimestampColumn()].concat(this.getBotColumns());
    this.displayedColumns = this.columns.map(c => c.columnDef);
    this.bots = this.getAllBotNames(this.dataSource.data);
  }

  private getTimestampColumn(): { columnDef: string; header: string; cell: (element: any) => string; } {
    return { columnDef: 'timestamp', header: 'Timestamp', cell: (element: any) => `${formatDate(new Date(element.timestamp * 1000), 'yyyy-MM-dd hh:mm', 'en-US')}` };
  }

  private getBotColumns(): ConcatArray<{ columnDef: string; header: string; cell: (element: any) => string; }> {
    return this.bots.map((x => {
      return { columnDef: x, header: x, cell: (element: ChallengeResult) => `${element.stats[x] !== undefined ? element.stats[x]["sum"] : ''}` };
    }));
  }

  private getAllBotNames(data: ChallengeResult[]) {
    let bots = data.flatMap(d => Object.keys(d.stats))
    // Only unique members ...
    return [... new Set(bots)]
  }
}

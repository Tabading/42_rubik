procedure CreateMoveTables;
begin
  CreateTwistMoveTable;
  CreateFlipMoveTable;
  CreateTetraMoveTable;
  CreateFlipUDSliceMoveTable;

  CreateUDSliceSortedMoveTable;
  CreateCornPermMoveTable;

  CreateGetCorn8PermTable;//für Coset-Explorer
//  CreateCorn8PermMoveTable;  //für den Coset Explorer (Prescan)

  CreateEdge8PermMoveTable;
  CreateUDSliceSortedSymMoveTable;

  CreateCentOriMoveTable; //needed for oriented Cubes
  CreateCentOriRFLBMod2MoveTable;
  CreateRFLBCentOriParityTable;
  CreateUDSliceParityTable;
  CreateUDSliceMoveTable;

end;

//  Create Move Table for the corner orientations
procedure CreateTwistMoveTable;
    var c: CubieCube; i,k: Integer; j,j1: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 2187-1 do
      begin
        if i and $fff =0 then Application.ProcessMessages;
        c.InvCornOriCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then TwistMove[i,Move(3*Ord(j)+k)]:=c.CornOriCoord;
          end;
        end;
      end;
      c.Free;
      Form1.ProgressBar.Position:=30;
    end;

//  Create Move Table for the edge orientations 
procedure CreateFlipMoveTable;
    var c: CubieCube; i,k: Integer; j: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 2048-1 do
      begin
        c.InvEdgeOriCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then FlipMove[i,Move(3*Ord(j)+k)]:=c.EdgeOriCoord;
          end;
        end;
      end;
      c.Free;
    end;


//  Create Move Table for the tetraeder coordinate 
procedure CreateTetraMoveTable;
        var c: CubieCube; i,k: Integer; j: TurnAxis;
        begin
          c:= CubieCube.Create;
          for i:=0 to 70-1 do
          begin
            c.InvTetraCoord(i);
            for j:= U to Fs do
            begin
              for k:= 0 to 3 do
              begin
                c.Move(j);
                if k<>3 then TetraMove[i,Move(3*Ord(j)+k)]:=c.TetraCoord;
              end;
            end;
          end;
          c.Free;
        end;

//  Create Move Table for the FlipUDSlice sym-coordinate 
procedure CreateFlipUDSliceMoveTable;
    var c: CubieCube; i,k,n: Integer; j: TurnAxis;
        fstr: TFileStream;
    const filename = 'flipUDslice.move';
    begin
      SetLength(FlipSliceMove,64430,27);//27 is number of different moves
      if FileExists(filename) then
      begin
        fstr := TFileStream.Create(filename, fmOpenRead);
        for k:= 0 to 64430-1 do
        begin
          fstr.ReadBuffer(FlipSliceMove[k][0],27*4);
          if k and $fff =0 then Application.ProcessMessages;
        end;
        Form1.ProgressBar.Position:=40;
      end
      else
      begin
        c:= CubieCube.Create;
        Form1.SetUpProgressBar(0,64430-1,'Creating '+filename+' (6.6 MB)');
        for i:=0 to 64430-1 do
        begin
          Form1.ProgressBar.Position:=i;
          if i and $fff =0 then Application.ProcessMessages;
          n:= FlipUDSliceToRawFlipUDSlice[i];
          c.InvUDSliceCoord(n div 2048);
          c.InvEdgeOriCoord(n mod 2048);
          for j:= U to Fs do
          begin
            for k:= 0 to 3 do //X1,X2,X3 (and X4=ID to restore Cube)
            begin
              c.Move(j);
              if k<>3 then FlipSliceMove[i,3*Ord(j)+k]:= c.FlipUDSliceCoord;
            end;
          end;
        end;
        fstr := TFileStream.Create(filename, fmCreate);
        for k:= 0 to 64430-1 do
          fstr.WriteBuffer(FlipSliceMove[k][0],27*4);
        c.Free;
        Form1.SetUpProgressBar(0,100,'Loading...');
      end;
      fstr.Free;
    end;


// =====================================================================================================================

//  Create Move Table for the UDSliceSorted raw-coordinate 
procedure CreateUDSliceSortedMoveTable;
    var c: CubieCube; i,k: Integer; j: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 11879 do
      begin
        if i and $fff = 0 then Application.ProcessMessages;
        c.InvUDSliceSortedCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then UDSliceSortedMove[i,Move(3*Ord(j)+k)]:=c.UDSliceSortedCoord;
          end;
        end;
      end;
      c.Free;
      Form1.ProgressBar.Position:=50;
    end;

//  Create Move Table for the Corner Permutations 
procedure CreateCornPermMoveTable;
    var c: CubieCube; i,k: Integer; j,j1: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 40320-1 do
      begin
        if i and $fff = 0 then Application.ProcessMessages;
        c.InvCornPermCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then CornPermMove[i,Move(3*Ord(j)+k)]:=c.CornPermCoord;
          end;
        end;
      end;
      c.Free;
      Form1.ProgressBar.Position:=60;
    end;


// =====================================================================================================================

procedure CreateGetCorn8PermTable;//falls Slicekoordinate
    Type Tetra1Corner = (URF1,UFL1,URB1,UBR1);
    //     Tetra2Corner = (DFR1,DLF1,DBL1,DRB1);
    var c:CubieCube; k,x1,x2,s: Integer; i1,j1: Tetra1Corner;
           test: array[URF..DRB] of Integer; cc: Corner;
    const
     Tetra1ToCorner: array [URF1..UBR1] of Corner =
     (URF,UFL,ULB,UBR);
    begin
      c:= CubieCube.Create;
      for k:=0 to 40320-1 do
      begin
        if k and $fff =0 then Application.ProcessMessages;
        c.InvCornPermCoord(k);
        //testen ob die ersten vier Koordinaten überhaupt im Tetraeder liegen
        for cc:= URF to DRB do test[cc]:=0;
        for i1:= URF1 to UBR1 do Inc(test[c.PCorn^[Tetra1ToCorner[i1]].c]);
        if test[URF]*test[UFL]*test[ULB]*test[UBR]<>1 then x1:=-1
        else
        begin
          x1:= 0;
          for i1:= UBR1 downto Succ(URF1) do
          begin
           s:=0;
           for j1:= Pred(i1) downto URF1 do
           begin
             if c.PCorn^[Tetra1ToCorner[j1]].c>c.PCorn^[Tetra1ToCorner[i1]].c then Inc(s);
            end;
            x1:= (x1+s)*Ord(i1);
          end;
        end;

    //ich habe ein besseres Gefühl, das auf die Position von zwei Steinen zu beziehen.
        if      (c.PCorn^[DFR].c=DFR) and (c.PCorn^[DLF].c=DLF) then x2:=0
        else if (c.PCorn^[DFR].c=DFR) and (c.PCorn^[DBL].c=DLF) then x2:=1
        else if (c.PCorn^[DFR].c=DFR) and (c.PCorn^[DRB].c=DLF) then x2:=2
        else if (c.PCorn^[DLF].c=DFR) and (c.PCorn^[DFR].c=DLF) then x2:=3
        else if (c.PCorn^[DLF].c=DFR) and (c.PCorn^[DBL].c=DLF) then x2:=4
        else if (c.PCorn^[DLF].c=DFR) and (c.PCorn^[DRB].c=DLF) then x2:=5
        else if (c.PCorn^[DBL].c=DFR) and (c.PCorn^[DFR].c=DLF) then x2:=6
        else if (c.PCorn^[DBL].c=DFR) and (c.PCorn^[DLF].c=DLF) then x2:=7
        else if (c.PCorn^[DBL].c=DFR) and (c.PCorn^[DRB].c=DLF) then x2:=8
        else if (c.PCorn^[DRB].c=DFR) and (c.PCorn^[DFR].c=DLF) then x2:=9
        else if (c.PCorn^[DRB].c=DFR) and (c.PCorn^[DLF].c=DLF) then x2:=10
        else if (c.PCorn^[DRB].c=DFR) and (c.PCorn^[DBL].c=DLF) then x2:=11
        else x2:=-1;

        if (x1=-1) or (x2=-1) then GetCorn8Perm[k]:=288 else GetCorn8Perm[k]:=12*x1+x2;
      end;
      c.free;
    end;


// =====================================================================================================================

//  Create Move Table for the phase 2 edge permutation coordinate 
procedure CreateEdge8PermMoveTable;
    var c: CubieCube; i,k: Integer; j: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 40320-1 do
      begin
       if i and $fff = 0 then Application.ProcessMessages;
       c.InvPhase2EdgePermCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            case j of
              U,D,Us:
              if k<3 then Edge8PermMove[i,Move(3*Ord(j)+k)]:=c.Phase2EdgePermCoord;
              R,L,F,B,Rs,Fs:
              if k=1 then Edge8PermMove[i,Move(3*Ord(j)+k)]:=c.Phase2EdgePermCoord;
            end;
          end;
        end;
      end;
      c.Free;
      Form1.ProgressBar.Position:=70;
    end;

//  Create Move Table for the UDSliceSorted sym-coordinate (used only in Big Optimal Solver)
procedure CreateUDSliceSortedSymMoveTable;
    var c: CubieCube; i,k: Integer; j: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 788-1 do
      begin
        c.InvUDSliceSortedSymCoord(i shl 4);//use the representants!!
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then UDSliceSortedSymMove[i,Move(3*Ord(j)+k)]:=c.UDSliceSortedSymCoord;
          end;
        end;
      end;
      c.Free;
    end;

// =====================================================================================================================

//  Create Move Table for the centers 
procedure CreateCentOriMoveTable;
    var c: CubieCube; i,k: Integer; j,j1: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 4096-1 do
      begin
        if i and $fff =0 then Application.ProcessMessages;
        c.InvCentOriCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then CentOriMove[i,Move(3*Ord(j)+k)]:=c.CentOriCoord;
          end;
        end;

      end;
      c.Free;
    end;

procedure CreateCentOriRFLBMod2MoveTable;
    var c: CubieCube; i,k: Integer; j: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 16-1 do
      begin
        c.InvCentOriRFLBMod2Coord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then CentOriRFLBMod2Move[i,Move(3*Ord(j)+k)]:=c.CentOriRFLBMod2Coord;
          end;
        end;
      end;
      c.Free;
    end;

procedure CreateRFLBCentOriParityTable;
    var c: CubieCube; i: Integer;
    begin
     c:= CubieCube.Create;
     for i:= 0 to 4096-1 do
     begin
       c.InvCentOriCoord(i);
       if c.RFLBCentOriParityEven
       then RFLBCentOriParity[i]:=0
       else RFLBCentOriParity[i]:=1;
     end;
     c.Free;
    end;

procedure CreateUDSliceParityTable;
    var c: CubieCube; i: Integer;
    begin
     c:= CubieCube.Create;
     for i:= 0 to 24-1 do
     begin
       c.InvUDSliceSortedCoord(i);
       if c.UDSliceParityEven
       then UDSliceParity[i]:=0
       else UDSliceParity[i]:=1;
     end;
     c.Free;
    end;

//  Create Move Table for the UDSliceCoord 
procedure CreateUDSliceMoveTable;
    var c: CubieCube; i,k: Integer; j: TurnAxis;
    begin
      c:= CubieCube.Create;
      for i:=0 to 495-1 do
      begin
        c.InvUDSliceCoord(i);
        for j:= U to Fs do
        begin
          for k:= 0 to 3 do
          begin
            c.Move(j);
            if k<>3 then UDSliceMove[i,Move(3*Ord(j)+k)]:=c.UDSliceCoord;
          end;
        end;
      end;
      c.Free;
    end;

// =====================================================================================================================
